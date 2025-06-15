package com.example.portfolio.api.common.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

  @GetMapping("/")
  public String index() {
    return "index";
  }

  @GetMapping("/index")
  public String indexpage() {
    return "index";
  }

  @GetMapping("/about")
  public String about() {
    return "about";
  }

  @GetMapping("/resume")
  public String resume() {
    return "resume";
  }

  @GetMapping("/service")
  public String services() {
    return "service";
  }

  @GetMapping("/projects")
  public String portfolio() {
    return "projects";
  }

  @GetMapping("/contact")
  public String contact() {
    return "temp";
  }
}
