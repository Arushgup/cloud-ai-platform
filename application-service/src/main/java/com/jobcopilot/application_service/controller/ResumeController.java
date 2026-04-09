package com.jobcopilot.application_service.controller;

import com.jobcopilot.application_service.entity.Resume;
import com.jobcopilot.application_service.service.ResumeService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/resume")
@RequiredArgsConstructor
public class ResumeController {

    private final ResumeService resumeService;

    @PostMapping
    public Resume upload(@RequestBody String content,
                         @RequestHeader("X-User-Email") String userEmail) {

        return resumeService.uploadResume(content, userEmail);
    }
}