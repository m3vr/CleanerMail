from datetime import date

def get_cleaners(residents, jobs, args):
    weekNumber = date.today().isocalendar()[1]
    if args.verbose: print(f"INFO: Weeknumber: {weekNumber}")

    cleaners = dict()

    workNumber = weekNumber * len(jobs) % len(residents)
    i = 0

    for job in jobs.keys():
        cleaners[job] = residents[(workNumber+i)%(len(residents))]
        if args.verbose: print(f"INFO: Cleaner: {job} = {residents[(workNumber+i)%(len(residents))]}")
        i += 1

    return cleaners
