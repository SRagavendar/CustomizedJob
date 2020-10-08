import re
import requests
from bs4 import BeautifulSoup

baseUrl = 'https://www.naukri.com/'
def get_organization(data):
	dummy = data.find_all('span', {'class': 'Rating'})
	org_name = dummy[0].text
	return org_name

def get_experience(data):
	dummy = data.find_all('span', {'class': 'Experience'})
	exp = 100
	if re.match('\d+', dummy[0].text):
		dummy = re.find_all('\d+',(dummy[0].text))
		for i in dummy:
			if re.match('\d+',i):
				if int(i) < exp:
					exp = int(i)
		return exp
	else:
		return 0

def get_location(data):
	dummy = data.find_all('span', {'class': 'Location'})
	if len(dummy) > 0:
		loc = dummy[0].text
		return loc
	else:
		return None

def get_skills(data):
	dummy = data.find_all('span', {'class', 'skill'})
    if len(dummy) > 0:
        skill = re.split('\s+ | ,+',dummy[0].text)
        print (skill)
        return skill
    else:
        return None

def get_description(data):
    dummy = data.find_all('span', {'class': 'desc'})
    if len(dummy) > 0:
        desc = dummy[0].text
        return desc
    else:
        return None

def convert_to_int(string_data):
    try:
        data = string_data.split(',')
        string_data = ''
        for i in data:
            string_data += i
        return int(string_data)
    except :
        return 0

def get_salary(data):
    salary_list=[]
    salary = data.find_all('span', {'class': 'salary'})
    try:
        if len(salary) > 0:
            salary = re.split('\s+ | (P\.A\.)+ | -+ | \w+',salary[0].text)
            for i in salary:
                if i is not None:
                    if re.match('\d+',i):
                        salary_list.append(convert_to_int(i))
            if len(salary_list)>0:
                return max(salary_list)
        else:
            return 0
    except:
        return 0

def get_info_from_each_tuple(data):
    dummy_dict = dict()
    dummy_dict['salary'] = get_salary(data)
    dummy_dict['company'] = get_organization(data)
    dummy_dict['loc'] = get_location(data)
    dummy_dict['skills'] = get_skills(data)
    dummy_dict['description'] = get_description(data)
    dummy_dict['exp'] = get_experience(data)
    return dummy_dict

def get_jobs_count(bsobj):
    dummy_regex = re.compile('\\d+')
    data = bsobj.find_all('span', {'class': 'cnt'})
    count_first = data[0].text
    count = count_first.split(" ")
    index = 0
    if re.search(dummy_regex, count_first) is not None:
        for i in count:
            if i == 'of':
                break
            else:
                index += 1
        count = int(count[index + 1])
        return count
    else:
        return 0

def make_obj(paramet, cnt):
    flg=0
    if int(cnt)==0:
        flg=1
    if flg!=1:
        new_url =base_url+str(paramet)+'-jobs'+'-'+str(cnt)
    else:
        new_url =base_url+str(paramet)+'-jobs'   
    url = requests.get(new_url)
    delay()
    bsobj = BeautifulSoup(url.text)
    return bsobj

def make_count(count):
    if count/50 > 1:
        return count//50
    if count!=0 and count/50 < 1:
        return (count+50)//50
    else:
        return 0
"""here pass the job specification of the containing individual jobs """

def delay():
    pass

def run_scraper(paramet):
    total_list_fetched=[]
    bsobj = make_obj(paramet, 0)
    check = bsobj.find_all('div', {'type': 'tuple'})
    a = 0
    if len(check) == 0:
    	pass
    else:
        count = get_jobs_count(bsobj)
        for i in range(int(make_count(count))):
            bsobj = make_obj(paramet, int(i))
            bsobj_len = bsobj.find_all('div', {'type': 'tuple'})
            for j in range(len(bsobj_len)):
                try:
                    total_list_fetched.append(get_info_from_each_tuple(bsobj_len[j]))
                    print("done", " ",a)
                    print (total_list_fetched[a])
                    a+=1
                    print (len(total_list_fetched))
                    if a > int(3000):
                        return total_list_fetched
                except:
                    j+=1
                    continue
        try:
            avg_l=[0,0,0,0,0,0] 
            sal_l=sorted(total_list_fetched,key=itemgetter('Salary'),reverse=True)
            exp_l=sorted(total_list_fetched,key=itemgetter('Experience'))
            if len(sal_l) > 0:
                for i in range(len[sal_l]):
                    if (sal_l[i])['Salary'] > 0:
                        avg_l[0]+=(sal_l[i])['Salary']
                        avg_l[3]+=1
            if len(exp_l) > 0:
                for i in range(len[exp_l]):
                    if (sal_l[i])['Experience'] is not None:
                        avg_l[1]+=(sal_l[i])['Experience']
                        avg_l[4]+=1
            avg_l[0]=avg_l[0]//avg_l[3]
            avg_l[1]=avg_l[1]//avg_l[4]
            avg_l[2]=len(total_list_fetched)
            avg_l=avg_l[:4]
            print ('Job computed')
            return total_list_fetched , avg_l
        except:
            pass
    return total_list_fetched

if __name__ == '__main__':