package com.target.casestudy.repository;

import com.target.casestudy.entity.ProductRepositoryInterface;
import com.target.casestudy.entity.Product;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;

import java.util.Map;

public class ProductRepositoryImpl implements ProductRepositoryInterface {

    @Autowired
    MongoTemplate mongoTemplate;

    @Override
    public void updatePriceInfo(Map<String,String> priceInfo,String id)
    {
        Product product = mongoTemplate.findOne(
                Query.query(Criteria.where("_id").is(id)), Product.class);
        product.setCurrent_price(priceInfo);
        mongoTemplate.save(product, "products");
    }
}
