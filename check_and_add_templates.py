from app import app, db
from models import WorksheetTemplate

def check_and_add_templates():
    with app.app_context():
        templates = WorksheetTemplate.query.all()
        print(f"Number of templates in the database: {len(templates)}")
        
        if len(templates) == 0:
            print("No templates found. Adding sample templates.")
            sample_templates = [
                WorksheetTemplate(
                    name="Multiple Choice",
                    description="A template for multiple choice questions",
                    template_type="quiz",
                    content="1. Question\n   a) Option 1\n   b) Option 2\n   c) Option 3\n   d) Option 4"
                ),
                WorksheetTemplate(
                    name="Fill in the Blanks",
                    description="A template for fill in the blanks questions",
                    template_type="quiz",
                    content="1. __________ is the capital of France.\n2. The largest planet in our solar system is __________."
                ),
                WorksheetTemplate(
                    name="Matching",
                    description="A template for matching questions",
                    template_type="quiz",
                    content="1. A) Item 1    [  ] Corresponding item\n2. B) Item 2    [  ] Corresponding item\n3. C) Item 3    [  ] Corresponding item"
                )
            ]
            for template in sample_templates:
                db.session.add(template)
            db.session.commit()
            print(f"Added {len(sample_templates)} sample templates.")
        else:
            for template in templates:
                print(f"Template ID: {template.id}, Name: {template.name}")

if __name__ == "__main__":
    check_and_add_templates()
