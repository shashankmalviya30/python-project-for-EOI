from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Change this to a secure key
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Routes for login, sign up, and logout
@app.route('/')
def index():
    # Check if user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username  # Store username in session
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/ask', methods=['POST'])
def ask():
    if 'username' not in session:
        return jsonify({'response': "Please log in to ask questions."})
    
    question = request.json['question']
    response = responses.get(question, "I'm sorry, I don't have information on that topic.")
    return jsonify({'response': response})

# Your responses dictionary
responses = {
    "Environmental regulations for coal mining?": "Environmental regulations include measures for air and water quality, land reclamation, and biodiversity protection. These regulations aim to minimize the environmental impact of coal mining operations.",
    "How to obtain coal mining permits?": "To obtain coal mining permits, applicants must submit detailed plans for environmental protection, safety measures, and reclamation. The permitting process involves thorough review and approval by regulatory agencies.",
    "Safety measures in coal mines?": "Safety measures in coal mines encompass various aspects such as ventilation systems, roof support, equipment maintenance, and emergency response plans. These measures are crucial for protecting the health and safety of miners.",
    "What is the CMSHA?": "The Coal Mine Safety and Health Act (CMSHA) is a federal law enacted to improve safety standards in coal mines. It establishes regulations for mine operators to ensure safe working conditions and prevent accidents.",
    "MSHA's role in coal mine safety?": "The Mine Safety and Health Administration (MSHA) is responsible for enforcing safety regulations in coal mines. MSHA conducts inspections, investigates accidents, and imposes penalties for non-compliance to ensure miner safety.",
    "What is SMCRA?": "The Surface Mining Control and Reclamation Act (SMCRA) is a federal law aimed at regulating surface coal mining operations. It requires operators to reclaim mined land to its pre-mining state, minimizing environmental damage.",
    "What is AML program?": "The Abandoned Mine Land (AML) program addresses environmental and safety hazards posed by abandoned coal mines. It funds reclamation projects to mitigate hazards and restore affected areas.",
    "Key provisions of FCMSA of 1952?": "The Federal Coal Mine Safety Act of 1952 established safety standards for coal mines, including requirements for ventilation, roof support, and methane detection.",
    "OSHA's role in coal mine safety?": "The Occupational Safety and Health Administration (OSHA) sets and enforces workplace safety standards, including those applicable to coal mines. OSHA conducts inspections and investigates complaints to ensure compliance.",
    "Penalties for violating regulations?": "Penalties for violating coal mining regulations may include fines, citations, and shutdown orders. Repeat violations or serious safety infractions can result in significant penalties.",
    "What is MINER Act?": "The Mine Improvement and New Emergency Response (MINER) Act is a federal law enacted in response to mining accidents. It enhances safety standards, requires improved emergency response plans, and enhances training for miners.",
    "Coal mining inspections procedure?": "Coal mining inspections involve thorough examinations of mining operations to ensure compliance with safety and environmental regulations. Inspectors assess various aspects such as equipment safety, ventilation systems, and emergency preparedness.",
    "What are reclamation requirements?": "Reclamation requirements for coal mining sites specify the steps operators must take to restore mined land to a usable or environmentally stable condition. This may include grading, seeding, and replanting vegetation.",
    "Difference between surface and underground mining regulations?": "Surface mining and underground mining regulations differ in terms of environmental impacts, safety measures, and operational requirements. Surface mining may have stricter reclamation requirements, while underground mining may focus more on ventilation and roof support.",
    "Reporting requirements for coal mine accidents?": "Coal mine operators are required to report accidents, injuries, and dangerous occurrences to regulatory agencies such as MSHA. This helps in investigating incidents, identifying root causes, and implementing preventive measures.",
    "Role of state regulatory agencies?": "State regulatory agencies play a role in overseeing coal mining operations within their jurisdictions. They may enforce state-specific regulations, conduct inspections, and collaborate with federal agencies on enforcement efforts.",
    "Significance of NEPA in coal mining?": "The National Environmental Policy Act (NEPA) requires federal agencies to assess the environmental impact of proposed projects, including coal mining activities. NEPA ensures that environmental considerations are integrated into decision-making processes.",
    "Health hazards associated with coal mining?": "Health hazards in coal mining include exposure to coal dust, silica dust, and diesel exhaust, which can lead to respiratory diseases such as black lung and chronic obstructive pulmonary disease (COPD). Miners may also face injuries from accidents and exposure to hazardous chemicals.",
    "Process for obtaining coal mining lease on federal lands?": "To obtain a coal mining lease on federal lands, applicants must follow a detailed application process administered by agencies such as the Bureau of Land Management (BLM). This process involves environmental assessment, public comment periods, and lease auctions.",
    "Requirements for coal mine ventilation systems?": "Coal mine ventilation systems are required to provide a continuous supply of fresh air to underground workings, dilute and remove contaminants, and maintain safe working conditions for miners. Ventilation requirements may vary based on mine size, depth, and layout.",
    "Purpose of Coal Workers' Health Surveillance Program?": "The Coal Workers' Health Surveillance Program monitors the health of coal miners and identifies early signs of occupational lung diseases such as pneumoconiosis (black lung disease). This program helps in assessing and preventing work-related health risks.",
    "Role of Federal Mine Safety and Health Review Commission?": "The Federal Mine Safety and Health Review Commission adjudicates disputes related to enforcement actions and penalties issued by MSHA. It ensures fairness and due process in the enforcement of mining regulations.",
    "Investigation process for coal mining accidents?": "Coal mining accidents are investigated by regulatory agencies such as MSHA to determine the cause, prevent recurrence, and hold accountable parties responsible for safety violations. Investigations may involve site inspections, witness interviews, and analysis of evidence.",
    "Process for reclaiming abandoned coal mine sites?": "Reclaiming abandoned coal mine sites involves restoring disturbed land to a usable or environmentally safe condition. This may include grading, recontouring, soil stabilization, and revegetation to mitigate erosion and improve habitat.",
    "Federal regulations for coal mine explosives handling?": "Federal regulations for coal mine explosives handling establish standards for storage, transportation, and use of explosives in mining operations. These regulations aim to prevent accidents, minimize environmental impacts, and ensure worker safety.",
    "What is the Black Lung Benefits Act?": "The Black Lung Benefits Act provides compensation and medical benefits to coal miners disabled by pneumoconiosis (black lung disease) or their dependents. It aims to support affected individuals and alleviate financial burdens associated with occupational lung diseases.",
    "Process for obtaining coal mining permits on Native American lands?": "To obtain coal mining permits on Native American lands, applicants must navigate a complex regulatory process involving tribal governments, federal agencies, and environmental assessments. This process may require consultation with tribal communities and compliance with tribal regulations.",
    "Significance of FCMHSA of 1969?": "The Federal Coal Mine Health and Safety Act of 1969 was a landmark legislation that established comprehensive health and safety standards for coal mines. It led to significant improvements in miner safety and health protections.",
    "Requirements for coal mine emergency response plans?": "Coal mine emergency response plans outline procedures for responding to accidents, fires, explosions, and other emergencies. These plans specify evacuation routes, communication protocols, emergency equipment, and coordination with local emergency responders.",
    "Impact of Mine Act on coal mining safety?": "The Mine Act strengthened safety and health protections for miners by expanding regulatory authority, enhancing enforcement powers, and establishing rights for miners to refuse unsafe work. It has contributed to significant reductions in mining accidents and fatalities.",
    # Add more question-response pairs as needed
}


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
