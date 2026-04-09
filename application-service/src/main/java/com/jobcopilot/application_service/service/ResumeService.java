package com.jobcopilot.application_service.service;

import com.jobcopilot.application_service.entity.Resume;
import com.jobcopilot.application_service.repository.ResumeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class ResumeService {

    private final ResumeRepository resumeRepository;
    private final KafkaTemplate<String, String> kafkaTemplate;

    public Resume uploadResume(String content, String userEmail) {

        Resume resume = Resume.builder()
                .content(content)
                .userEmail(userEmail)
                .createdAt(LocalDateTime.now())
                .build();

        resumeRepository.save(resume);

        kafkaTemplate.send("resume-uploaded", resume.getId().toString());

        return resume;
    }
}