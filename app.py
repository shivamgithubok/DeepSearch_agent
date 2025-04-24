"""
Flask web application for the Deep Research AI Agent System
"""
import os
import logging
import json
from datetime import datetime
import markdown
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from markupsafe import Markup
# from flask_sqlalchemy import SQLAlchemy

from workflows.research_workflow import run_research_workflow
from utils.file_utils import save_research_results, save_draft
import config
# from models import db, Research, Finding, Draft

# Set up the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", os.urandom(24).hex())

# Configure database (commented out)
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
# app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
#     "pool_recycle": 300,
#     "pool_pre_ping": True,
# }
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database (commented out)
# db.init_app(app)

# Create database tables (commented out)
# with app.app_context():
#     from sqlalchemy import inspect
#     inspector = inspect(db.engine)
#     existing_tables = inspector.get_table_names()
#     if not all(table in existing_tables for table in ['researches', 'findings', 'drafts']):
#         db.create_all()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Render the home page with the search form"""
    return render_template('index.html')

@app.route('/research', methods=['POST'])
def research():
    """Process the research request and return results"""
    query = request.form.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        research_results, draft_content = run_research_workflow(query)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        research_file = save_research_results(research_results, query, timestamp)
        draft_file = save_draft(draft_content, query, timestamp)
        
        # Database interaction (commented out)
        # research_entry = Research(query=query)
        # db.session.add(research_entry)
        # db.session.flush()
        
        # for finding in research_results:
        #     finding_entry = Finding(
        #         research_id=research_entry.id,
        #         title=finding.get('title', 'Untitled'),
        #         content=finding.get('content', ''),
        #         source_url=finding.get('source_url', ''),
        #         source_title=finding.get('source_title', 'Unknown Source')
        #     )
        #     db.session.add(finding_entry)
        
        # draft_entry = Draft(
        #     research_id=research_entry.id,
        #     content=draft_content
        # )
        # db.session.add(draft_entry)
        # db.session.commit()
        
        session['query'] = query
        session['research_results'] = json.dumps(research_results)
        session['draft'] = draft_content
        session['research_file'] = research_file
        session['draft_file'] = draft_file
        # session['research_id'] = research_entry.id
        session['research_id'] = "no_db"

        return redirect(url_for('results'))

    except Exception as e:
        logger.exception("Error in research workflow")
        # db.session.rollback()
        return jsonify({'error': f'Research failed: {str(e)}'}), 500

@app.route('/results')
def results():
    if 'query' not in session:
        return redirect(url_for('index'))
    
    query = session.get('query')
    research_results = json.loads(session.get('research_results', '[]'))
    draft = session.get('draft', '')
    research_file = session.get('research_file', '')
    draft_file = session.get('draft_file', '')
    research_id = session.get('research_id')

    html_draft = Markup(markdown.markdown(draft, extensions=['tables', 'fenced_code']))

    return render_template(
        'results.html',
        query=query,
        research_results=research_results,
        draft=html_draft,
        research_file=research_file,
        draft_file=draft_file,
        research_id=research_id
    )

@app.route('/history')
def history():
    """History route - disabled without DB"""
    # research_entries = Research.query.order_by(Research.created_at.desc()).all()
    research_entries = []  # Empty placeholder
    return render_template('history.html', researches=research_entries)

@app.route('/research/<int:research_id>')
def view_research(research_id):
    """Disabled detailed view without DB"""
    # research = Research.query.get_or_404(research_id)
    # findings = Finding.query.filter_by(research_id=research_id).all()
    # draft = Draft.query.filter_by(research_id=research_id).first()
    findings = []
    draft = None
    html_draft = None

    return render_template(
        'results.html',
        query="(DB-disabled view)",
        research_results=findings,
        draft=html_draft,
        research_id=research_id,
        from_database=True
    )

@app.route('/api/research', methods=['POST'])
def api_research():
    data = request.json
    query = data.get('query', '') if data else ''
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        research_results, draft_content = run_research_workflow(query)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        research_file = save_research_results(research_results, query, timestamp)
        draft_file = save_draft(draft_content, query, timestamp)
        
        # research_entry = Research(query=query)
        # db.session.add(research_entry)
        # db.session.flush()
        
        # for finding in research_results:
        #     finding_entry = Finding(
        #         research_id=research_entry.id,
        #         title=finding.get('title', 'Untitled'),
        #         content=finding.get('content', ''),
        #         source_url=finding.get('source_url', ''),
        #         source_title=finding.get('source_title', 'Unknown Source')
        #     )
        #     db.session.add(finding_entry)
        
        # draft_entry = Draft(
        #     research_id=research_entry.id,
        #     content=draft_content
        # )
        # db.session.add(draft_entry)
        # db.session.commit()
        
        return jsonify({
            'query': query,
            'research_results': research_results,
            'draft': draft_content,
            'research_file': research_file,
            'draft_file': draft_file,
            # 'research_id': research_entry.id
            'research_id': "no_db"
        })

    except Exception as e:
        logger.exception("Error in research workflow")
        # db.session.rollback()
        return jsonify({'error': f'Research failed: {str(e)}'}), 500

@app.route('/main_app')
def main_app_view():
    return "Server is running correctly!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)
