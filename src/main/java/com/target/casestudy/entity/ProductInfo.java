package com.target.casestudy.entity;

import com.mongodb.annotations.Beta;
import org.springframework.context.annotation.Bean;

import java.math.BigDecimal;
import java.util.Map;


public class ProductInfo {

    String productId;
    String productTitle;
    Map<String,String> price;

    public String getProductId() {
        return productId;
    }

    public void setProductId(String productId) {
        this.productId = productId;
    }

    public String getProductTitle() {
        return productTitle;
    }

    public void setProductTitle(String productTitle) {
        this.productTitle = productTitle;
    }

    public Map<String, String> getPrice() {
        return price;
    }

    public void setPrice(Map<String, String> price) {
        this.price = price;
    }
}
