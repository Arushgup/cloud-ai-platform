package com.jobcopilot.application_service.repository;

import com.jobcopilot.application_service.entity.Resume;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ResumeRepository extends JpaRepository<Resume, Long> {
}