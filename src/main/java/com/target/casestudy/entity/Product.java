package com.target.casestudy.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Transient;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Map;

@Document(collection="products")
public class Product {

    @Id
    public String productId;
    @Transient
    public String title;

    public Map<String, String> current_price;

    public Product() {
    }

    public Product(String productId, String title, Map<String, String> current_price) {
        this.productId = productId;
        this.title = title;
        this.current_price = current_price;
    }

    public String getProductId() {
        return productId;
    }

    public void setProductId(String productId) {
        this.productId = productId;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public Map<String, String> getCurrent_price() {
        return current_price;
    }

    public void setCurrent_price(Map<String, String> current_price) {
        this.current_price = current_price;
    }
}
