def build_elasticsearch_query(input):
    must_clauses = [
        {"term": {"is_parent": 1}},
        {"term": {"deleted": 0}}
    ]
    
    if input.get('location'):
        must_clauses.append({
            "match": {
                "location": input['location']
            }
        })
    
    if input.get('company') and input.get('job_title'):
        company_clause = {
            "nested": {
                "path": "experience",
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase": {
                                    "experience.company_name": f"\"{input['company']}\""
                                }
                            },
                            {
                                "match_phrase": {
                                    "experience.title": input['job_title']
                                }
                            },
                            {
                                "term": {
                                    "experience.deleted": 0
                                }
                            }
                                                
                        ]
                    }
                }
            }
        }
        must_clauses.append(company_clause)
    
    if input.get('job_title') and not input.get('company'):
        company_clause = {
            "nested": {
                "path": "experience",
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase": {
                                    "experience.title": input['job_title']
                                }
                            },
                            {
                                "term": {
                                    "experience.deleted": 0
                                }
                            }
                        ]
                    }
                }
            }
        }
        must_clauses.append(company_clause)
    
    if input.get('company') and not input.get('job_title'):
        company_clause = {
            "nested": {
                "path": "experience",
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase": {
                                    "experience.company_name": f"\"{input['company']}\""
                                }
                            },
                            {
                                "term": {
                                    "experience.deleted": 0
                                }
                            }
                                                
                        ]
                    }
                }
            }
        }
        must_clauses.append(company_clause)
    
    if input.get('education_institution') and input.get('major'):
        education_clause = {
            "nested": {
                "path": "education",
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase": {
                                    "education.institution": f"\"{input['education_institution']}\""
                                }
                            },
                            {
                                "match_phrase": {
                                    "education.program": input['major']
                                }
                            },
                            {
                                "term": {
                                    "education.deleted": 0
                                }
                            }
                        ]
                    }
                }
            }
        }
        must_clauses.append(education_clause)
    
    if input.get('education_institution') and not input.get('major'):
        education_clause = {
            "nested": {
                "path": "education",
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase": {
                                    "education.institution": f"\"{input['education_institution']}\""
                                }
                            },
                            {
                                "term": {
                                    "education.deleted": 0
                                }
                            }
                        ]
                    }
                }
            }
        }
        must_clauses.append(education_clause)
    
    if not input.get('education_institution') and input.get('major'):
        education_clause = {
            "nested": {
                "path": "education",
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "education.program": input['major']
                                }
                            },
                            {
                                "term": {
                                    "education.deleted": 0
                                }
                            }
                        ]
                    }
                }
            }
        }
        must_clauses.append(education_clause)
    
    
    if input.get('skills'):
        must_clauses.append({
            "nested": {
                "path": "skills",
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "skills.skill": input['skills']
                                }
                            }
                        ]
                    }
                }
            }
        })
    
    query = {
        "query": {
            "bool": {
                "must": must_clauses
            }
        }
    }
    
    return query