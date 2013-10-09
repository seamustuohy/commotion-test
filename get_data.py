import re
import os
import json

def main(date=None, directory="logs"):
    """
    """
    
    if date == None:
        for dirs,logsdir,files in os.walk(directory):
            if re.match("logs/(.*)", dirs):
                log_date = re.match("logs/(.*)", dirs).group(1)
                results = {}
                for log in files:
                    results[log_date+log] = get_logs(dirs, log)
                write_data(log_date, results)
    else:
        date_dir = "logs/"+date+".+"
        for dirs,logsdir,files in os.walk(directory):
            results = {}
            if re.match(date_dir, dirs):
                for log in files:
                    log_date = re.match(date_dir, dirs).group(0)
                    results[log_date] = {log:get_logs(dirs, log)}
                write_data(log_date, results)
            
def get_logs(directory, log):
    """
    parses logs and passes them to the parser
    """
    full_log = open(directory+"/"+log, "r")
    log_text = full_log.read()
    time_split = "(Test Time\: \d{4}\-\d{2}\-\d{2} \d{2}\:\d{2}\:\d{2})\n?"
    tests = re.split(time_split, log_text)
    tests.pop(0) #If there are capturing groups in the separator and it matches at the start of the string, the result will start with an empty string.
    #tests[0] = time #tests[1] = logs
    log_parsers = {
        "connection":parse_connection,
        "iperf":parse_iperf,
        "leases":parse_leases,
        }
    parsed_log = {}
    time_of_test = None
    test_identified = None
    for i in tests:
        #print(time_of_test, test_identified, i[0:32])
        if test_identified:
            #print("starting parsing process")
            #print(i[0:23])
            #print(time_of_test[0])
            parsed_log[time_of_test[0]] = {"logs":log_parsers[log](i)} #uses the log file name to determine the function to use to parse
            time_of_test = None
            test_identified = None
        else:
            time_of_test = re.findall("Test Time\: (\d{4}\-\d{2}\-\d{2} \d{2}\:\d{2}\:\d{2})", i)
        if time_of_test:
            test_identified = True
    return parsed_log

def parse_connection(logs):
    """ Identifies the connection test being passed to it and returns the parsed results.
    """
    parsed_results = None
    re_ip = "\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}"
    if re.match("Average ping time to", logs) or re.match(re_ip+" could not be reached", logs):
        parsed_results = {"ping test": parse_ping_time(logs)}
    #else:
    #    print("not a ping ")
    #print(logs)
    elif re.match("Active Internet connections", logs):
        parsed_results = {"netstat test":parse_netstat(logs)}
    if parsed_results:
        return parsed_results

def parse_ping_time(pings):
    """takes a set of ping attempts and returns a tuple with the ip address and the mili-seconds to that ping result or the result FAILED if the attempt failed, which seems pretty intuitive to me.
    """
    result = []
    ip_regex = "\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}"
    milisec_regex = "\d*\.\d*"
    all_pings = re.split("\n", pings)
    for ping in all_pings:
        if re.match("A", ping):
            cur_result = re.match(".+?("+ip_regex+") was ("+milisec_regex+").*", ping)
            result.append({"ip_addr":cur_result.group(1), "milisecs":cur_result.group(2)})
        else:
            cur_result = re.match("("+ip_regex+").*", ping)
            if cur_result:
                result.append({"ip_addr":cur_result.group(1), "milisecs":"FAILED"})
    return result

def parse_netstat(netstat):
    """Does nothing but return a snippy statement because I can't think of a use for the netstat logs currently. """
    return "netstat logs are not useless but data intensive and not useful for parsing at this time."

    
def parse_leases(logs):
    """
    splits up the nodog splash files for individual routers and passes them to get further parsed and then return a set of tuples to the above once completed.
    """
    parsed_results = {}
    nodog = "={18}\nNoDogSplash Status\n={4}\n"
    stati = re.split(nodog, logs)
    for status in stati:
        #print("["+status+"]\n%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
        if status != '':
            ip_addr, data = parse_nodog(status)
            parsed_results[ip_addr] = data
    if parsed_results:
        return parsed_results

def parse_nodog(logs):
    """
    iterates through a nodog splash status config to identify the various compnents and place then in a nested list. passes back a tuple containing the splash overall status and a dictionary of clients and usage.
    """
    status = {}
    clients = {}
    properties = {
        "uptime":"^Uptime: (.*)$",
        "total_dl":"^Total download: (.*?) avg: .*$",
        "avrg_dl":"^Total download:.*?avg: (.*)$",
        "total_ul":"^Total upload: (.*?) avg: .*$",
        "avrg_ul":"^Total upload:.*?avg: (.*)$",
        "client_auths":"^Client authentications since start: (.*)$",
        "current_clients":"^Current clients: (.*)$"
        }
    client_properties = {
        "ip":"^  IP: (.*?) MAC.*$",
        "added":"^  Added: (.*?)$",
        "active":"^  Active: (.*?)$",
        "total_dl":"^  Download: (.*?);.*$",       
        "avrg_dl":"^  Download:.*?avg: (.*)$",
        "total_ul":"^  Upload: (.*?);.*$",
        "avrg_ul":"^  Upload:.*?avg: (.*)$",
        "active_duration":"^  Active duration: (.*)$",
        "added_duration":"^  Added duration:  (.*)$",
        }

    for i in properties:
        status[i] = re.search(properties[i], logs, re.MULTILINE).group(1)
    ip_addr = re.search("^Server listening: (.*?):", logs, re.MULTILINE).group(1)
#    print(logs)
    raw_clients = re.findall("(Client \d.*?\n\n)", logs, re.DOTALL)
    for client in raw_clients:
        mac = "^  IP: .*? MAC: (.*)$"
        MAC = re.search(mac, client, re.MULTILINE).group(1)
        clients[MAC]={}
        for i in client_properties:
            clients[MAC][i] = re.search(client_properties[i], client, re.MULTILINE).group(1)
    """
    for i in clients:
        print(i)
        for n in clients[i]:
            print(n)
    """
    return ip_addr, (status, clients)
    
def parse_iperf(logs):
    """
    """
    parsed_results = {}
    ip_regex = "\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}"
    group_split = "Destination: (.*)\n"
    all_tests = re.split(group_split, logs)
    all_tests.pop(0) #Odd that they add that '' on a first char match
    destination = None
    for test in all_tests:
        if destination:
            re_trace = re.search("^(traceroute.*?)\-{60}" ,test, re.DOTALL)
            if re_trace:
                traceroute = parse_traceroute(re_trace.group(1))
            else:
                traceroute = "FAILED TRACEROUTE"
            re_perf = re.search("^traceroute.*?\-{60}(.*)" ,test, re.DOTALL)
            if re_perf:
                iperf = parse_iperf_test(re_perf.group(1))
            else:
                iperf = "FAILED IPERF"
            parsed_results[destination[0]] = {"traceroute":traceroute, "iperf":iperf}
            destination = None
        else:
            destination = re.findall("("+ip_regex+")", test)
    return parsed_results

def parse_traceroute(trace):
    results = []
    ip_regex = "\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}"
    milisecs = "\d{0,3}\.\d{0,3}"
    single_hop = "^ (\d)  ("+ip_regex+")  ("+milisecs+").*?("+milisecs+").*?("+milisecs+")"
    hop_count = 0
    for hop, next_ip, one, two, three  in re.findall(single_hop, trace, re.MULTILINE):
        if hop > hop_count:
            hop_count = hop
        avg_rnd_trp = (float(one) + float(two) + float(three))/float(3)
        results.append({"ip":next_ip, "avg_rnd_trp":avg_rnd_trp})
    results.append({"hop_count":hop_count})
    return(results)


def parse_iperf_test(test):
    results = {}
    ip_regex = "\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}"
    re_header = "("+ip_regex+").*?\-{60}.*?"
    re_test_head = "\[\s+?\d\]\slocal\s+?("+ip_regex+").*?"+ip_regex
    full_head = re_header+re_test_head
    #get header info
    destination, ip = re.search(full_head, test, re.DOTALL).group(1,2)
    results['dest'] = destination
    results['local_ip'] = ip
    #iterate through results to get interval, tranfer and byandwidth
    re_int = "0.0\-\d{0,4}\.?\d{0,4}\s\w+"
    re_trans = "\d{0,4}\.?\d{0,4}\s\w+"
    re_band = "\d{0,4}\.?\d{0,4}\s\w+\/\w+"
    re_result = "\[  \d\]\s+("+re_int+")\s+("+re_trans+")\s+("+re_band+").*$"
    raw_result = re.findall(re_result, test, re.MULTILINE)[0]
    interval, transfer, bandwidth = raw_result[0], raw_result[1], raw_result[2]
    results['transfer'] = transfer
    results['interval'] = interval
    results['bandwidth'] = bandwidth
    return results

def write_data(date, data):
    
    json.dump(str(data), outfile)
    #    print(date)
#    print("\n")
#    print(json.dumps(data, sort_keys=True, indent=2))
    """
    print("==============================data==============================")
    print(date)
    for i in data:
        print(i)
    print("================================================================")
    """
    pass

if __name__ == "__main__":
    #main("2013\-10\-03")
    my_database = []
    with open("dataset", "w") as outfile:
        main()
    outfile.close()
