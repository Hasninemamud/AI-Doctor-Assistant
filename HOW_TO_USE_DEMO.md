# How to Use the Demo Health Issue

This guide explains how to test your AI Doctor Assistant app using the comprehensive demo health issue provided.

## Demo Files Created

1. **DEMO_HEALTH_ISSUE.md** - Complete patient scenario and expected analysis
2. **demo_blood_work.txt** - Sample CBC lab results
3. **demo_headache_diary.txt** - 21-day symptom tracking log
4. **demo_bp_log.txt** - Blood pressure monitoring data

## Step-by-Step Demo Instructions

### 1. Access the Landing Page
- Open `http://localhost:3000/` in your browser
- If logged in, log out first to see the landing page
- Review the comprehensive guidance and features

### 2. Create Account (if needed)
- Click "Get Started" or "Register"
- Create a demo account or use existing credentials

### 3. Start New Consultation
- Navigate to "New Consultation" from the app dashboard
- Enter the chief complaint:
  ```
  "I've been experiencing severe headaches for the past 3 weeks, often accompanied by visual disturbances and nausea. The headaches are getting worse and more frequent."
  ```

### 4. Input Detailed Symptoms
Use the symptom form to enter:

**Primary Complaint**: Severe recurring headaches
**Duration**: 3 weeks
**Severity**: 6-9/10 (escalating)
**Associated Symptoms**:
- Visual aura/disturbances
- Nausea and vomiting
- Light sensitivity (photophobia)
- Sound sensitivity (phonophobia)
- Temporary speech difficulties

**Triggers Identified**:
- Prolonged screen time (>6 hours)
- Bright/fluorescent lights
- Stress from work
- Poor sleep
- Skipping meals

**Timeline Entries** (add these chronologically):
- Week 1: Mild headaches, increasing frequency
- Week 2: Severe episodes with visual aura
- Week 3: Worst headaches with new symptoms (speech difficulties)

### 5. Upload Medical Documents
Upload the three demo files:
1. **demo_blood_work.txt** as "Recent Lab Results"
2. **demo_headache_diary.txt** as "Symptom Diary"
3. **demo_bp_log.txt** as "Blood Pressure Log"

### 6. Request AI Analysis
- Submit for comprehensive AI analysis
- The system should detect:
  - **Primary concern**: Migraine headaches with aura
  - **Risk level**: Moderate to High
  - **Emergency flags**: Speech difficulties, persistent visual changes
  - **Pattern detection**: Escalating frequency and severity

### 7. Expected AI Response Categories

**Immediate Actions (Critical)**:
- Monitor for red flag symptoms
- Seek neurological evaluation within 48 hours
- Document any new or worsening symptoms

**Medical Follow-up (High Priority)**:
- Primary care appointment within 1 week
- Neurology referral recommended
- Consider brain imaging (MRI)
- Blood pressure evaluation

**Lifestyle Modifications (High Priority)**:
- Limit screen time to 2-hour intervals
- Establish regular sleep schedule
- Identify and avoid known triggers
- Stay hydrated, eat regular meals

**Self-Care Measures (Medium Priority)**:
- Dark, quiet environment during episodes
- Cold compress therapy
- Stress management techniques
- Track symptoms in diary

**Emergency Warning Signs** (Critical to note):
- Sudden severe "thunderclap" headache
- Headache with fever/neck stiffness
- Persistent vision changes
- Confusion or speech problems

### 8. Test Key Features

**Pattern Detection**: 
- App should identify the 3-week progression
- Detect correlation between triggers and episodes
- Note escalating severity pattern

**Risk Assessment**:
- Should flag speech difficulties as concerning
- Identify blood pressure elevation pattern
- Note medication overuse developing

**Emergency Detection**:
- Should highlight speech symptoms as urgent
- Flag persistent visual changes
- Recommend immediate medical evaluation

**Timeline Analysis**:
- Track symptom progression over time
- Identify trigger patterns
- Show severity trending upward

## What to Look For in the Demo

### ✅ Successful Features to Verify:
- Comprehensive symptom intake form
- File upload functionality for multiple document types
- AI analysis that provides structured, prioritized recommendations
- Clear risk level assessment
- Emergency warning identification
- Medical disclaimer prominently displayed
- User-friendly presentation of complex medical information

### 🔍 Test Different Scenarios:
- Try uploading different file formats (PDF, images, text)
- Test with incomplete information
- Verify mobile responsiveness
- Check error handling for invalid inputs

### 📊 Expected Analytics Results:
- **Confidence Level**: 85-90% for migraine diagnosis
- **Risk Classification**: Moderate to High
- **Urgency Level**: Within 48 hours for specialist
- **Pattern Strength**: Strong correlation with triggers

## Demo Script for Presentations

"Let me show you how Sarah, a 34-year-old software developer, uses our AI Doctor Assistant for her concerning headache symptoms..."

1. **Landing Page**: "Sarah visits our app and learns how to get primary medical guidance..."
2. **Symptom Input**: "She describes her 3-week progression of worsening headaches..."
3. **Document Upload**: "Sarah uploads her blood work, symptom diary, and BP monitoring..."
4. **AI Analysis**: "Our AI identifies this as likely migraine with concerning features requiring prompt medical attention..."
5. **Results**: "Sarah receives structured guidance prioritized by urgency and category..."

## Educational Value

This demo showcases:
- **Real-world complexity**: Realistic patient presentation
- **Progressive symptoms**: Shows how conditions evolve
- **Multiple data sources**: Integrates various medical documents
- **Risk stratification**: Demonstrates appropriate urgency levels
- **Patient empowerment**: Provides actionable guidance while emphasizing professional care

## Safety Notes

⚠️ **Always emphasize in demos**:
- This is for educational/preliminary guidance only
- Professional medical evaluation is essential
- Emergency symptoms require immediate care
- AI cannot replace qualified healthcare providers

The demo effectively demonstrates how your app provides valuable primary-level medical support while maintaining appropriate medical boundaries and safety protocols.