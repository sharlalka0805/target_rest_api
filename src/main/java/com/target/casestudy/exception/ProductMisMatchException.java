package com.target.casestudy.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "ProductId in request header and body are different")
public class ProductMisMatchException extends RuntimeException {

    private static final long serialVersionUID = 1L;
    public ProductMisMatchException() {
    }
}
