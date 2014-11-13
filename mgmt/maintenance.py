
from django.shortcuts import render

# TODO: when adding new vendor, add maintenance task to celery

def update_contracts_by_vendor(request): # TODO NEW TASK for celery
    from datetime import datetime as DT
    from datetime import timedelta
    from aporo.settings import DAYS_SCHEDULED_AHEAD,DG_K_PERIOD,UTC_OFFSET_hr
    from django.db.models import F
    from aporo.models import Vendor,Contract
    """
    Starting with Active Vendors with StartDate equal to or less than today,
    of all Vendor_Sched where last_processed is blank,
    create DG_Sched entries.
    """
    def adjust_for_timezone(this_datetime,new_hr,UTC_OFFSET_hr):
        save_hour = new_hr+UTC_OFFSET_hr
        if save_hour < 0:
            prev_day = this_datetime - timedelta(days=1)
            t = prev_day.timetuple()[:3]+(24+save_hour,0)
        elif 0 <= save_hour <= 23:
            t = this_datetime.timetuple()[:3]+(save_hour,0)
        elif save_hour > 23:
            next_day = this_datetime + timedelta(days=1)
            t = next_day.timetuple()[:3]+(24-save_hour,0)
        return DT(*t)
    def process_contracts_by_date(v,start_date,end_date):
        p_start_date = start_date - timedelta(days=1)
        p_end_date = end_date - timedelta(days=1)
        for V in v.iterator():
            weekdays = V.days
            start_times = V.start_times
            end_times = V.end_times
            AREA = V.area
            holidays = V.holidays

            # TODO: incorporate holidays & DST in scheduling/maintenance

            # weekdays='Mon,Tue-Fri,Sat,Sun'
            # start_times='11:00 am, 9:00 am, 1:00 pm, 2:00 pm'
            # end_times='11:00 pm, 11:00 pm, 9:00 pm, 8:00 pm'
            weekdays,start_times,end_times = weekdays.split(','),start_times.split(','),end_times.split(',')

            daygenerator = (p_start_date + timedelta(days=(x + 1)) for x in xrange((p_end_date - p_start_date).days))
            day_dict = {'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5,'Sun':6}

            for i in range(0,len(weekdays)):
                day_group = weekdays[i]
                if len(day_group)==3: s_day,e_day = day_dict[day_group],day_dict[day_group]
                else:
                    s_day,e_day=[day_dict[it] for it in day_group.split('-')]

                s,e = DT.strptime(start_times[i].strip(),'%I:%M %p'),DT.strptime(end_times[i].strip(),'%I:%M %p')
                s_hour,s_min,e_hour,e_min = s.hour,s.minute,e.hour,e.minute

                for d in daygenerator:
                    if s_day <= d.weekday() <= e_day:

                        for dg_start_hr in range(0,24,DG_K_PERIOD):
                            a,b = dg_start_hr,DG_K_PERIOD+dg_start_hr
                            if b<s_hour or e_hour<a: pass
                            else:

                                if s_hour<a: start_pt = a
                                elif a<=s_hour<=b: start_pt = s_hour

                                if a<=e_hour<=b: end_pt = e_hour
                                elif b<e_hour: end_pt = b

                                vendor_hours = end_pt - start_pt
                                # TODO: apply wgt to vendor_units, where wgt=cumsum( a function generated weekly for each V based in history )
                                additional_vendor_units = vendor_hours

                                sdt = adjust_for_timezone(d,dg_start_hr,UTC_OFFSET_hr)
                                k = Contract.objects.get(start_datetime=sdt,
                                                         area=AREA)
                                k.vendor_units = F('vendor_units') + additional_vendor_units
                                k.is_open = True
                                k.save()

            t = start_date.timetuple()[:3]+(start_date.hour,start_date.minute)
            V.last_processed = DT(*t)
            r = end_date.timetuple()[:3]+(start_date.hour,start_date.minute)
            V.processed_through = DT(*r)
            V.save()

    start_date = DT.today()
    end_date = start_date + timedelta(days=DAYS_SCHEDULED_AHEAD)
    start_str, end_str = start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    v = Vendor.objects.filter(is_active=True,processed_through__isnull=True)
    process_contracts_by_date(v,start_date,end_date)

    v = Vendor.objects.filter(is_active=True,processed_through__range=[start_str, end_str])
    process_contracts_by_date(v,start_date,end_date)

    return render(request, 'management/success.html', {})

def create_empty_contracts_by_datetime(request):
    from datetime import datetime as DT
    from datetime import timedelta
    from aporo.settings import DAYS_SCHEDULED_AHEAD,DG_K_PERIOD,UTC_OFFSET_hr
    from app.models import Contract

    start_date = DT.today()
    end_date = start_date + timedelta(days=DAYS_SCHEDULED_AHEAD)
    start_str, end_str = start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    q = Contract.objects.filter(start_datetime__range=[start_str, end_str])
    q_ct = q.count()

    # TODO: query vendors and obtain list of areas to iterate over
    areas = ['Murray Hill']

    # for AREA in areas:  # iterate this function
    AREA = areas[0]

    if q_ct == 0: skip_db_check = True
    else: skip_db_check = False

    k,k_iter = 1,q.iterator()
    try:
        dg_sched = k_iter.next()
        this_area = dg_sched.area
    except StopIteration:
        skip_db_check = True
        this_area = AREA

    def daterange(start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(days=n)
    def update_dg_sched(k,k_iter,q_ct):
        if k+1>q_ct: return 0,0
        else:
            k+=1
            return k,k_iter
    def adjust_for_timezone(this_datetime,new_hr,UTC_OFFSET_hr):
        save_hour = new_hr+UTC_OFFSET_hr
        if save_hour < 0:
            prev_day = this_datetime - timedelta(days=1)
            t = prev_day.timetuple()[:3]+(24+save_hour,0)
        elif 0 <= save_hour <= 23:
            t = this_datetime.timetuple()[:3]+(save_hour,0)
        elif save_hour > 23:
            next_day = this_datetime + timedelta(days=1)
            t = next_day.timetuple()[:3]+(24-save_hour,0)
        return DT(*t)
    def append_contract(x,single_date,hr,this_area):
        s = adjust_for_timezone(single_date,hr,0)
        t = adjust_for_timezone(single_date,hr,UTC_OFFSET_hr)
        x.append( Contract( start_datetime=t,
                            start_day=s.strftime('%a, %b. %d'),
                            start_time=s.strftime('%I:%M %p'),
                            hour_period=DG_K_PERIOD,
                            area=this_area) )
        return x
    def make_all_contracts_in_range(single_date):
        x= []
        for hr in range(0,24,DG_K_PERIOD):
            x = append_contract(x,single_date,hr,this_area)
        return x
    def make_some_contracts_in_range(single_date,dg_sched):
        x=[]
        for hr in range(0,24,DG_K_PERIOD):
            if hr == dg_sched.start_datetime.hour: pass
            else:
                x = append_contract(x,single_date,hr,this_area)
        return x

    # TODO: while dg_sched.area == this_area: ...
    # TODO: if dg_sched.area changes, then cycle needs to break
    # TODO: if still more dg_sched, repeat while loop

    bulk_contracts = []
    for single_date in daterange(start_date, end_date):
        if skip_db_check == True:   # which means no more dg_sched left
            bulk_contracts.extend( make_all_contracts_in_range(single_date) )
        else:
            while dg_sched.start_datetime < single_date:
                k,k_iter = update_dg_sched(k,k_iter,q_ct)
                if k==0:
                    skip_db_check = True
                    break
                else: dg_sched = k_iter.next()

                if dg_sched.start_datetime >= single_date: break

            if skip_db_check == True:
                bulk_contracts.extend( make_all_contracts_in_range(single_date) )

            elif single_date.timetuple()[:3] == dg_sched.start_datetime.timetuple()[:3]:
                bulk_contracts.extend( make_some_contracts_in_range(single_date,dg_sched) )
                k,k_iter=   update_dg_sched(k,k_iter,q_ct)
                if k==0:    skip_db_check = True
                else:       dg_sched = k_iter.next()

    Contract.objects.bulk_create( bulk_contracts )

    return render(request, 'management/success.html', {})
