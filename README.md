HeartGuard AI – Heart Disease Prediction Platform
Hey there! 👋 I built HeartGuard AI as a complete machine learning solution that helps predict heart disease risk. It's more than just a model — it's a full web application with user accounts, admin features, and analytics that's actually ready to use.
🎯 What It Does
This app lets users input their medical data and get an instant prediction about their heart disease risk. Everything is saved, tracked, and visualized. Plus, there's an admin panel to oversee everything happening on the platform.
✨ Cool Features I Built

🔐 Secure Login System – Sign up, log in, passwords are properly hashed
🧠 Smart Predictions – Machine learning model trained on real heart disease data
📊 Performance Tracking – See how accurate the model is in real-time
📁 Personal History – Every user can view their past predictions
📈 Visual Analytics – Charts showing prediction trends
🛠 Admin Panel – Overview of all users and predictions
💾 Database Backend – SQLite storing everything securely
🌐 Live & Deployed – Running on Streamlit Cloud

🛠 Built With
Python • Streamlit • Scikit-learn • Pandas • NumPy • SQLite • Matplotlib
🧠 About The Model
I used Logistic Regression because it's reliable and interpretable for medical predictions.

Training Accuracy: ~88%
Testing Accuracy: ~79%
Input Features: 13 medical attributes (age, blood pressure, cholesterol, etc.)

The model was trained on the UCI Heart Disease dataset with an 80-20 train-test split.
🔒 Security Features
Since this deals with health data, I made sure to implement proper security:

Passwords hashed with SHA-256 (not stored as plain text!)
Session-based authentication
Role-based access (regular users vs admin)

📊 Admin Dashboard
Admins get a bird's-eye view:

List of all registered users
Complete prediction history across all users
Visual breakdown of prediction distribution

📂 How It's Organized
HeartGuard_AI/
│
├── app.py              # Main application
├── train_model.py      # Model training script
├── heart_model.pkl     # Trained model
├── Heart.csv           # Dataset
├── requirements.txt    # Dependencies
└── README.md           # You're reading it!
💭 My Development Process
I handled everything from concept to deployment:
The ML Side:

Cleaned and explored the dataset
Trained and tested the Logistic Regression model
Saved the model for production use

The Development Side:

Built the entire Streamlit interface from scratch
Set up secure authentication with password hashing
Created the SQLite database schema and integration
Designed the admin dashboard with analytics
Deployed to Streamlit Cloud

Working Smart:
I used AI tools like ChatGPT to speed things up — getting help with UI layouts, refining code structure, and debugging tricky parts. But all the architectural decisions, problem-solving, integration work, and final code? That was me.
🎓 What I Learned
This project pushed me to:

Build a complete ML pipeline, not just train a model
Implement real authentication and security
Design user-friendly interfaces
Deploy a production-ready application
Work efficiently with AI assistance tools

🚀 What's Next?
Some ideas I'm considering:

Upgrade to PostgreSQL for better scaling
Add JWT authentication
Generate downloadable PDF reports
Integrate with real hospital APIs

🌐 Try It Live
The app is deployed and running! Feel free to check it out or fork the repo to experiment yourself.
⚠️ Quick Note
This is a learning project and demonstration tool. Always consult real healthcare professionals for medical advice!
🤝 Want to Contribute?
Found a bug? Have an idea? Open an issue or submit a PR — I'd love to collaborate!

Built by Keshav Chelmeti
If you found this helpful or interesting, a ⭐ would mean a lot!
