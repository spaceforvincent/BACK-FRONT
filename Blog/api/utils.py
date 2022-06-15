def obj_to_post(obj,flag=True):
    """
    obj의 각 속성을 serialize해서 dict로 변환한다
    serialize : python object -> int,str, float
    :param obj:
    :param flag: True(모두 보냄, /api/post/99/), False(일부 보냄, /api/post/list)
    :return:
    """
    post = dict(vars(obj))
    #blogapp의 models.py에서 char, int 필드들은 제외
    
    
    if obj.category:
        post['category'] = obj.category.name
    else:
        post['category'] = 'NoCategory'
    
    if obj.tags:
        post['tags'] = [t.name for t in obj.tags.all()]
    else:
        post['tags'] = []
    
    if obj.image:
        post['image'] = obj.image.url
    else:
        post['image'] = 'https://via.placeholder.com/900x300'
    
    if obj.updated_at:
        post['updated_at'] = obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        post['updated_at'] = '9999-12-31 00:00:00'


    del post['_state'], post['category_id'], post['created_at'], post['prefetched_objects_cache']
    if not flag:
        del post['tags'],post['updated_at'], post['description'], post['content']
    
    return post

def obj_to_comment(obj):
    """
    comment 객체를 serialize한다.
    """
    comment = dict(vars(obj)) #object를 dictionary로 형 변환
    #blogapp의 models.py에서 char, int 필드들은 제외하고 serialize한다
    #ex) content는 이미 str타입이므로 updated_at만 serialize해주면 된다
    
    
    if obj.updated_at:
        comment['updated_at'] = obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        comment['updated_at'] = '9999-12-31 00:00:00'


    del comment['_state'], comment['post_id'], comment['created_at'] #불필요한 필드들 삭제
    
    return comment


def prev_next_post(obj):
    try:
        prevObj = obj.get_previous_by_updated_at()
        prevDict = {
            'id' : prevObj.id,
            'title': prevObj.title,
        }
    except obj.DoesNotExist:
        prevDict = {}
    
    try:
        nextObj = obj.get_next_by_updated_at()
        nextDict = {
            'id' : nextObj.id,
            'title': nextObj.title,
        }
    except obj.DoesNotExist:
        nextDict = {}
    
    return prevDict, nextDict