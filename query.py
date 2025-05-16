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
    
    if input.get('company'):
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
        
        if input.get('job_title'):
            company_clause["nested"]["query"]["bool"]["must"].append({
                "match": {
                    "experience.title": input['job_title']
                }
            })
            
        must_clauses.append(company_clause)
    
    if input.get('education_institution'):
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
        
        if input.get('major'):
            education_clause["nested"]["query"]["bool"]["must"].append({
                "match": {
                    "education.program": input['major']
                }
            })
            
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

# # Example usage:
# input_data = {
#     "location": "",
#     "company": "",
#     "job_title": "",
#     "education_institution": "Stanford University",
#     "major": "",
#     "skills": ""
# }

# query = build_elasticsearch_query(input_data)

# print(query)