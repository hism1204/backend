from re import I
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from .models import *



'''#크랙 정보 목록 조회(노동자)
def show_user_crack_list(request, user_id):
    
    list=[]

    cursor = connection.cursor()
    query = f"select raw_data.raw_data_id,building.name,picture,floor,room,details\
        from glass join building on glass.target_building = building.building_id\
        join raw_data on glass.user_id = raw_data.upload_user_id\
        join issue on issue.raw_data_id = raw_data.raw_data_id\
        join account on glass.user_id = account.user_id\
        where account.user_id = '{user_id}';"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    
    col = "raw_data_id,name,picture,floor,room,details".split(",")

    for i in data:
        list.append(dict(zip(col,i)))

    crack_list = {'crack_list' : list}

    return JsonResponse(crack_list)'''

#크랙 정보 목록 조회(노동자)
def show_user_crack_list(request, user_id):

    #model에서 queryset 추출
    raw_data_id = Raw_data.objects.filter(upload_user_id__exact=user_id).values('raw_data_id')
    upload_target_building_id = Raw_data.objects.filter(upload_user_id__exact=user_id).values('upload_target_building_id')
    upload_building_name = Building.objects.filter(building_id__in=upload_target_building_id).values('building_name')
    picture = Raw_data.objects.filter(upload_user_id__exact=user_id).values('picture')
    information = Issue.objects.filter(issue_id__in=raw_data_id).values('floor','room','details')
    
    #추출한 queryset을 python list로 변환
    raw_data_id_result = [entry for entry in raw_data_id]
    upload_building_name_result = [entry for entry in upload_building_name]
    picture_result = [entry for entry in picture]
    information_result = [entry for entry in information] 

    #변환한 list들을 dict로 묶어주기
    crack_list = [dict(i,**j,**k,**l) for i,j,k,l in zip(raw_data_id_result,upload_building_name_result,picture_result,information_result)]

    #연결 여부 조회, 사용자가 다른 글래스에 연결되어 있으면 1, 연결되어 있지 않으면 0
    connected_user = Glass.objects.values('user_id')
    connected_user_result = [entry['user_id'] for entry in connected_user]
    print(connected_user_result)
    if user_id in connected_user_result:
        is_connected = 1
    else:
        is_connected = 0
    
    #최종으로 보낼 data
    data = {"admin":0,"is_connected":is_connected,"title":"내가 발견한 안전문제","issue_list":crack_list}


    return JsonResponse(data,json_dumps_params={'ensure_ascii': False})

'''#크랙 정보 목록 조회(관리자)
def show_manager_crack_list(request, user_id):
    
    list=[]

    cursor = connection.cursor()
    query = f"with company(manager_company_id) as( \
        select company_id from account where user_id = '{user_id}'\
    )\
    select raw_data.raw_data_id,building.name,picture,floor,room,details\
    from glass join building on glass.target_building = building.building_id\
    join raw_data on glass.user_id = raw_data.upload_user_id\
    join issue on issue.raw_data_id = raw_data.raw_data_id\
    join account on glass.user_id = account.user_id\
    where account.company_id in (select manager_company_id from company);"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()

    col = "raw_data_id,name,picture,floor,room,details".split(",")

    for i in data:
        list.append(dict(zip(col,i)))

    crack_list = {'crack_list' : list}

    return JsonResponse(crack_list)'''

def show_manager_crack_list(request, user_id):

    #접속 admin의 company 파악
    user_company = Account.objects.filter(user_id__exact=user_id).values('company_id')
    print(user_company)

    #접속 admin과 같은 company에 소속되어 있는 user만 추출
    user_list = Account.objects.filter(company_id__exact=user_company[0]['company_id']).values('user_id')&Account.objects.exclude(user_id__exact=user_id).values('user_id')
    print(user_list)

    #raw_data_id,name,picture,floor,room,details
    raw_data_id = Raw_data.objects.filter(upload_user_id__in=user_list).values('raw_data_id')
    upload_target_building_id = Raw_data.objects.filter(raw_data_id__in=raw_data_id).values('upload_target_building_id')
    picture = Raw_data.objects.filter(upload_user_id__in=user_list).values('picture')
    information = Issue.objects.filter(issue_id__in=raw_data_id).values('floor','room','details')

    #추출한 queryset을 python list로 변환
    raw_data_id_result = [entry for entry in raw_data_id]
    picture_result = [entry for entry in picture]
    information_result = [entry for entry in information] 

    #변환한 list들을 dict로 묶어주기
    crack_list = [dict(i,**j,**k) for i,j,k in zip(raw_data_id_result,picture_result,information_result)]

    #building_id와 매치되는 building_name 추가
    for i in range(len(upload_target_building_id)):
        '''building_name = Building.objects.filter(building_id__exact=crack_list[i]['upload_target_building_id']).values('building_name')[0]['building_name']
        crack_list[i]['name'] = building_name'''
        building_name = Building.objects.filter(building_id__exact=upload_target_building_id[i]['upload_target_building_id']).values('building_name')[0]['building_name']
        crack_list[i]['name'] = building_name

    data = {"admin":1,"title":"새 이슈","issue_list":crack_list}
    return JsonResponse(data,json_dumps_params={'ensure_ascii': False})

'''#연결할 글래스 선택
def show_glass_list(request):
    list=[]
    cursor = connection.cursor()
    query = "select glass_name from glass;"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    print(data)
    col = ["glass_name"]
    
    for i in data:
        list.append(dict(zip(col,i)))

    glass_list = {'glass_list' : list}

    return JsonResponse(glass_list)'''

#연결할 glass 선택
def show_glass_list(request,user_id):

    #접속 user의 company에서 관리하는 glass만 선택
    user_company = Account.objects.filter(user_id__exact=user_id).values('company_id')
    glass = Glass.objects.filter(company_id__exact=user_company[0]['company_id']).values('glass_id','glass_name','user_id')
    print(glass)

    #enable 설정, user_id가 None이면 enable=0, else enable=1
    for i in range(len(glass)):
        if glass[i]['user_id'] is None:
            glass[i]['enable'] = 0
        else:
            glass[i]['enable'] = 1

    #Queryset을 python list로 변환
    glass_list = [entry for entry in glass]

    #list에서 불필요한 data(user_id) 제거
    for i in range(len(glass_list)):
        del(glass_list[i]['user_id'])
    
    #최종 보낼 data
    data = {"glass_list":glass_list}

    return JsonResponse(data,json_dumps_params={'ensure_ascii': False})

'''#연결할 건물 선택
def show_building_list(request,user_id):
    list=[]
    cursor = connection.cursor()
    query = f" with company(user_company_id) as(\
        select company_id from account where user_id = 'user'\
    )\
    select name from building\
    where building.company_id in (select user_company_id from company)"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
   
    col = ['name']

    for i in data:
        list.append(dict(zip(col,i)))

    building_list = {'building_list' : list}

    return JsonResponse(building_list)'''

#연결할 건물 선택
def show_building_list(request,user_id):
    
    #접속 user의 company에 속한 building만 선택
    user_company = Account.objects.filter(user_id__exact=user_id).values('company_id')
    building = Building.objects.filter(company_id__exact=user_company[0]['company_id']).values('building_id','building_name')
    print(building)

    #Queryset을 python list로 변환
    building_list = [entry for entry in building]

    #최종 보낼 data
    data = {"building_list":building_list}

    return JsonResponse(data,json_dumps_params={'ensure_ascii': False})

#s3에서 이미지 받아서 db에 저장


#user가 선택한 building,glass 등록
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def connect_glass_and_building(request):
    try:
        request = json.loads(request.body)
        user_id = request['user_id']
        building_id = request['building_id']
        glass_id = request['glass_id']
    
        glass = Glass.objects.get(glass_id=glass_id)
        print(glass)
        glass.user_id = user_id
        glass.building_id = building_id
        glass.save()
        
        message = {"connect_message":"연결에 성공하였습니다."}
        return JsonResponse(message,json_dumps_params={'ensure_ascii': False})

    except:
        message = {"connect_message":"연결에 실패하였습니다."}
        return JsonResponse(message,json_dumps_params={'ensure_ascii': False})

#연결되어 있는 glass 해제
def disconnect_glass_and_building(request,user_id):
    try:
        glass = Glass.objects.get(user_id=user_id)
        glass.user_id = None
        glass.building_id = None
        glass.save()

        message = {"disconnect_message":"연결해제에 성공하였습니다."}
        return JsonResponse(message,json_dumps_params={'ensure_ascii': False})

    except:
        message = {"disconnect_message":"연결해제에 실패하였습니다."}
        return JsonResponse(message,json_dumps_params={'ensure_ascii': False})

def show_glass_list2(request,user_id):
    
    #접속 user의 company에서 관리하는 glass만 선택
    user_company = Account.objects.filter(user_id__exact=user_id).values('company_id')
    glass = Glass.objects.filter(company_id__exact=user_company[0]['company_id']).values('glass_id','glass_name','user_id','building_id')
    
    #Queryset을 python list로 변환
    glass_list = [entry for entry in glass]
   
    #building_id와 user_id를 이용하여 building_name과 user_name 추출
    for i in range(len(glass_list)):
        user_name = Account.objects.filter(user_id__exact=glass_list[i]['user_id']).values('name')
        building_name = Building.objects.filter(building_id__exact=glass_list[i]['building_id']).values('building_name')
       
        if not building_name and not user_name:
            glass_list[i]['building_name'] = None
            glass_list[i]['user_name'] = None
        else:
            glass_list[i]['building_name'] = building_name[0]['building_name']
            glass_list[i]['user_name'] = user_name[0]['name']

    #enable 설정, user_id가 None이면 enable=0, else enable=1
    for i in range(len(glass_list)):
        if glass_list[i]['user_id'] is None:
            glass_list[i]['enable'] = 0
        else:
            glass_list[i]['enable'] = 1
        
    #list에서 불필요한 data(user_id,building_id) 제거
    for i in range(len(glass_list)):
        del(glass_list[i]['user_id'])
        del(glass_list[i]['building_id'])

    join = Glass.objects.select_related('account').get(glass_id=1).account.name
    print(join)
    #최종 보낼 data
    data = {"admin":1,"glass_list":glass_list}

    return JsonResponse(data,json_dumps_params={'ensure_ascii': False})


def show_list(request,user_id):

    #admin 여부 판별
    is_admin = Account.objects.filter(user_id__exact=user_id).values('is_admin')
 
    #접속자가 user인 경우
    if is_admin[0]['is_admin'] == 0:
        
        #model에서 queryset 추출
        raw_data_id = Raw_data.objects.filter(upload_user_id__exact=user_id).values('raw_data_id')
        upload_target_building_id = Raw_data.objects.filter(upload_user_id__exact=user_id).values('upload_target_building_id')
        upload_building_name = Building.objects.filter(building_id__in=upload_target_building_id).values('building_name')
        picture = Raw_data.objects.filter(upload_user_id__exact=user_id).values('picture')
        information = Issue.objects.filter(issue_id__in=raw_data_id).values('floor','room','details')
        
        #추출한 queryset을 python list로 변환
        raw_data_id_result = [entry for entry in raw_data_id]
        upload_building_name_result = [entry for entry in upload_building_name]
        picture_result = [entry for entry in picture]
        information_result = [entry for entry in information] 

        #변환한 list들을 dict로 묶어주기
        crack_list = [dict(i,**j,**k,**l) for i,j,k,l in zip(raw_data_id_result,upload_building_name_result,picture_result,information_result)]

        #연결 여부 조회, 사용자가 다른 글래스에 연결되어 있으면 1, 연결되어 있지 않으면 0
        connected_user = Glass.objects.values('user_id')
        connected_user_result = [entry['user_id'] for entry in connected_user]
        print(connected_user_result)
        if user_id in connected_user_result:
            is_connected = 1
        else:
            is_connected = 0
        
        #최종으로 보낼 data
        data = {"admin":0,"is_connected":is_connected,"title":"내가 발견한 안전문제","issue_list":crack_list}


        return JsonResponse(data,json_dumps_params={'ensure_ascii': False})


    #접속자가 admin인 경우
    elif is_admin[0]['is_admin'] == 1:
        
        #접속 admin의 company 파악
        user_company = Account.objects.filter(user_id__exact=user_id).values('company_id')
       

        #접속 admin과 같은 company에 소속되어 있는 user만 추출
        user_list = Account.objects.filter(company_id__exact=user_company[0]['company_id']).values('user_id')&Account.objects.exclude(user_id__exact=user_id).values('user_id')
        

        #raw_data_id,name,picture,floor,room,details
        raw_data_id = Raw_data.objects.filter(upload_user_id__in=user_list).values('raw_data_id')
        upload_target_building_id = Raw_data.objects.filter(raw_data_id__in=raw_data_id).values('upload_target_building_id')
        picture = Raw_data.objects.filter(upload_user_id__in=user_list).values('picture')
        information = Issue.objects.filter(issue_id__in=raw_data_id).values('floor','room','details')
        

        #추출한 queryset을 python list로 변환
        raw_data_id_result = [entry for entry in raw_data_id]
        picture_result = [entry for entry in picture]
        information_result = [entry for entry in information] 
       
        #변환한 list들을 dict로 묶어주기
        crack_list = [dict(i,**j,**k) for i,j,k in zip(raw_data_id_result,picture_result,information_result)]
        
        #building_id와 매치되는 building_name 추가
        for i in range(len(upload_target_building_id)):
            '''building_name = Building.objects.filter(building_id__exact=crack_list[i]['upload_target_building_id']).values('building_name')[0]['building_name']
            crack_list[i]['name'] = building_name'''
            building_name = Building.objects.filter(building_id__exact=upload_target_building_id[i]['upload_target_building_id']).values('building_name')[0]['building_name']
            
            crack_list[i]['name'] = building_name

         #접속 user의 company에 속한 building만 선택
        user_company = Account.objects.filter(user_id__exact=user_id).values('company_id')
        building = Building.objects.filter(company_id__exact=user_company[0]['company_id']).values('building_id','building_name')
        print(building[0]['building_name'])

        #Queryset을 python list로 변환
        #building_list = [entry for entry in building]

        building_list=["전체"]
        for i in range(len(building)):
            building_list.append(building[i]['building_name'])

        
        print(building_list)
        data = {"admin":1,"title":"새 이슈","issue_list":crack_list,"building list":building_list}

        return JsonResponse(data,json_dumps_params={'ensure_ascii': False})
            
    
    

