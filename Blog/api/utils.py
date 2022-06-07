def obj_to_post(obj):
    """
    obj의 각 속성을 serialize해서 dict로 변환한다
    serialize : python object -> int,str, float
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
        post['image'] = 'https://via.placeholder.com/900x400'
    
    if obj.updated_at:
        post['updated_at'] = obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        post['updated_at'] = '9999-12-31 00:00:00'


    del post['_state'], post['category_id'], post['created_at']
    
    return post