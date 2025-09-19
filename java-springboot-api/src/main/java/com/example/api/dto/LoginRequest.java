package com.example.api.dto;

public class LoginRequest {
    private String username;
    private String password;
    public String getUsername(){return this.username;}
    public void setUsername(String u){this.username=u;}
    public String getPassword(){return this.password;}
    public void setPassword(String p){this.password=p;}
}
