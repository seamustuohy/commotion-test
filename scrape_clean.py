import clean_data1
import re

def main():
    sorted_dates = {}
    data = clean_data1.data
    for i in data:
        for key in i.keys():
            date = re.match("\d{4}\-\d{2}\-\d{2}",key).group(0)
            if date in sorted_dates.keys():
                sorted_dates[date].append(i[key])
            else:
                sorted_dates[date] = [i[key],]
    for i in sorted_dates:
#        print("+++++++++++++++"+i+"+++++++++++++++++++")
        for time in sorted_dates[i]:
            for logs in time.keys():
                for x in time[logs].keys():
                    #single ip addr == iperf
                    #'ping test' = ping test
                    #'netstat test' = nothing
                    #list of ip's = leases or iperf
                    if time[logs][x]:
                        if 'ping test' in time[logs][x].keys():
                            pass
                            #print("ping test")
                            #print(time[logs][x]['ping test'])
                        elif  len(time[logs][x].keys()) > 1:
#                            print(type(time[logs][x].keys()))
                            for lease_file in time[logs][x].keys():
                                if type(time[logs][x][lease_file]) == dict:
                                    for con_test in time[logs][x][lease_file].keys():
                                        con_test_res = time[logs][x][lease_file][con_test]
                                        if con_test_res != 'FAILED IPERF' and con_test_res != 'FAILED TRACEROUTE':
                                            if type(con_test_res) == dict:
                                                connections_iperf(con_test_res)
                                            
                                        #print(time[logs][x][lease_file][con_test])
                                else:
                                    pass
                                    #print("LEASES")
                                    #print(time[logs][x][lease_file])
                        elif 'netstat test' in time[logs][x].keys():
                            pass
                        elif re.match(ip_regex, time[logs][x].keys()[0]):
                            ip_a = re.match(ip_regex, time[logs][x].keys()[0]).group(0)
#                            print(ip_a)
                            if time[logs][x][ip_a]['iperf'] != 'FAILED IPERF':
                                connections_iperf(time[logs][x][ip_a]['iperf'])

def connections_iperf(test):
#    print("connections")
    iperf_fields = {'transfer':transfer, 'bandwidth':bandwidth, 'interval':interval}
    local_ip = test['local_ip']
    if local_ip in compiled_data.keys():
        dest_ip = test['dest']
        if dest_ip in compiled_data[local_ip].keys():
            for result in iperf_fields:
                if result in compiled_data[local_ip][dest_ip].keys():
                    compiled_data[local_ip][dest_ip][result] = iperf_fields[result](test[result], compiled_data[local_ip][dest_ip][result])
                else:
                    compiled_data[local_ip][dest_ip][result] = iperf_fields[result](test[result])
        else:
            compiled_data[local_ip][dest_ip] = {}
            for result in iperf_fields:
                compiled_data[local_ip][dest_ip][result] = iperf_fields[result](test[result])
    else:
        compiled_data[local_ip] = {}
        dest_ip = test['dest']
        compiled_data[local_ip][dest_ip] = {}
        for result in iperf_fields:
            compiled_data[local_ip][dest_ip][result] = iperf_fields[result](test[result])

def transfer(one, two=None):
    if two==None:
        return [float(re.match("\d{0,4}\.?\d{0,4}", one).group(0)),]
    else:
        a = float(re.match("\d{0,4}\.?\d{0,4}", one).group(0))
        three = []
        for i in two:
           three.append(i)
        three.append(a)
        return three

def bandwidth(one, two=None):
    if two==None:
        return [float(re.match("\d{0,4}\.?\d{0,4}", one).group(0)),]
    else:
        a = float(re.match("\d{0,4}\.?\d{0,4}", one).group(0))
        three = []
        for i in two:
           three.append(i)
        three.append(a)
        return three

def interval(one, two=None):
    if two==None:
        return [float(re.match("0.0\-(\d{0,4}\.?\d{0,4})", one).group(1)),]
    else:
        a = float(re.match("0.0\-(\d{0,4}\.?\d{0,4})", one).group(1))
        three = []
        for i in two:
           three.append(i)
        three.append(a)
        return three


if __name__ == "__main__":
    ip_regex = "\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}"
    compiled_data = {}
    main()
    for i in compiled_data:
        print(i, compiled_data[i])
        print("\n")
