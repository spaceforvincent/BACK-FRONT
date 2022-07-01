module.exports = {
  productList: {
    query:
      "select t1.*, t2.category1, t2.category2, t2.category3 , t3.path\
        from t_product t1, t_category t2, t_image t3\
        where t1.category_id = t2.id and t1.id = t3.product_id and t3.type=1",
  },
  productList2: { // 이미지가 등록되지 않았더라도 일단은 데이터를 갖고 오기
    query: `select t3.*, t4.path from (select t1.*, t2.category1, t2.category2, t2.category3 
      from t_product t1, t_category t2
      where t1.category_id = t2.id) t3
      left join (select * from t_image where type=1) t4
      on t3.id = t4.product_id`
  },
  productDetail: {
    query:
    "select t1.*, t2.category1, t2.category2, t2.category3, t3.path\
     from t_product t1, t_category t2, t_image t3\
     where t1.id = ? and t1.category_id = t2.id and t1.id = t3.product_id and t3.type = 3",
  },
  productMainImages: {
    query: "select * from t_image where product_id=? and type=2",
  },
  productInsert: {
    query:
      "insert into t_product set ?",
  },
  productImageInsert: {
    query: "insert into t_image (product_id, type, path) values (?, ?, ?)",
  },
  categoryList: {
    query: "select * from t_category",
  },
  sellerList: {
    query: "select * from t_seller",
  },
  signUp: {
    query: "insert into t_user set ? on duplicate key update ?" //없으면 넣고 있으면 업데이트
  },
  productDelete: {
    query: "delete from t_product where id=?"
  }
};
