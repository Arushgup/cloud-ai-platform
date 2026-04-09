package com.jobcopilot.application_service.repository;

import com.jobcopilot.application_service.entity.Job;
import org.springframework.data.jpa.repository.JpaRepository;

public interface JobRepository extends JpaRepository<Job, Long> {
}