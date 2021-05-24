class appLogger:
    def __init__(self
                 ,model_name
                 ,question_asked_time
                 ,question_text
                 ,answer_sent_time
                 ,answer_text
                 ,created_time
                 ,created_by
                 ,modified_time
                 ,modified_by):
        self.model_name = model_name
        self.question_asked_time = question_asked_time
        self.question_text = question_text
        self.answer_sent_time = answer_sent_time
        self.answer_text = answer_text
        self.created_time = created_time
        self.created_by = created_by
        self.modified_time = modified_time
        self.modified_by = modified_by

