import re


def contents_cleansing(contents):
    # 앞에 필요없는 부분 제거
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd> <span>', '',str(contents)).strip()  
    #뒤에 필요없는 부분 제거 (새끼 기사)
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd> </span>', '', first_cleansing_contents).strip()
    third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
    
    return third_cleansing_contents