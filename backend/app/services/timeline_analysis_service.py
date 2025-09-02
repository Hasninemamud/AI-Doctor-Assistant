# Timeline Analysis Service for Symptom Pattern Detection

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import statistics
import re
from dataclasses import dataclass
from enum import Enum

from app.services.specialized_medical_service import (
    SymptomTimelineEntry, TimelinePattern, specialized_medical_service
)


class TimelineAnalysisType(str, Enum):
    """Types of timeline analysis"""
    RAPID_ONSET = "rapid_onset"
    PROGRESSIVE_WORSENING = "progressive_worsening"
    CYCLICAL_PATTERN = "cyclical_pattern"
    SYMPTOM_CLUSTERING = "symptom_clustering"
    SEVERITY_TREND = "severity_trend"
    TEMPORAL_ASSOCIATION = "temporal_association"


@dataclass
class SymptomCluster:
    """Group of related symptoms appearing together"""
    symptoms: List[str]
    timeframe: Tuple[datetime, datetime]
    frequency: int
    clinical_significance: str


@dataclass
class SeverityTrend:
    """Trend analysis for symptom severity"""
    symptom: str
    trend_direction: str  # increasing, decreasing, stable, fluctuating
    slope: float  # rate of change
    correlation_coefficient: float
    significance: str


class SymptomTimelineAnalyzer:
    """Advanced symptom timeline analysis with pattern detection"""
    
    def __init__(self):
        self.emergency_keywords = [
            "chest pain", "difficulty breathing", "shortness of breath",
            "severe headache", "loss of consciousness", "seizure",
            "severe bleeding", "severe abdominal pain", "stroke symptoms",
            "heart palpitations", "severe allergic reaction", "overdose",
            "suicidal thoughts", "severe dizziness", "fainting"
        ]
        
        self.symptom_categories = {
            "cardiovascular": ["chest pain", "palpitations", "shortness of breath", "swelling", "fatigue"],
            "neurological": ["headache", "dizziness", "confusion", "memory loss", "seizure", "weakness"],
            "gastrointestinal": ["nausea", "vomiting", "diarrhea", "abdominal pain", "constipation"],
            "respiratory": ["cough", "shortness of breath", "wheezing", "chest tightness"],
            "musculoskeletal": ["joint pain", "muscle pain", "stiffness", "swelling"],
            "psychological": ["anxiety", "depression", "mood changes", "sleep problems"]
        }
    
    async def analyze_comprehensive_timeline(
        self,
        timeline: List[SymptomTimelineEntry],
        current_symptoms: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive timeline analysis
        
        Args:
            timeline: Chronological symptom entries
            current_symptoms: Current symptom state
            
        Returns:
            Dict containing comprehensive timeline analysis
        """
        if not timeline:
            return self._create_empty_analysis()
        
        # Sort timeline chronologically
        sorted_timeline = sorted(timeline, key=lambda x: x.timestamp)
        
        # Perform various analyses
        rapid_onset_patterns = self._detect_rapid_onset(sorted_timeline)
        severity_trends = self._analyze_severity_trends(sorted_timeline)
        cyclical_patterns = self._detect_cyclical_patterns(sorted_timeline)
        symptom_clusters = self._identify_symptom_clusters(sorted_timeline)
        temporal_associations = self._find_temporal_associations(sorted_timeline)
        emergency_indicators = self._detect_emergency_patterns(sorted_timeline)
        
        # Get AI-powered timeline analysis
        ai_analysis = await specialized_medical_service.symptom_timeline_analysis(
            sorted_timeline, current_symptoms
        )
        
        # Calculate overall risk assessment
        risk_assessment = self._calculate_comprehensive_risk(
            sorted_timeline, rapid_onset_patterns, severity_trends, emergency_indicators
        )
        
        # Generate recommendations based on patterns
        recommendations = self._generate_timeline_recommendations(
            rapid_onset_patterns, severity_trends, cyclical_patterns, 
            emergency_indicators, risk_assessment
        )
        
        return {
            "timeline_metadata": {
                "total_entries": len(sorted_timeline),
                "date_range": {
                    "start": sorted_timeline[0].timestamp.isoformat(),
                    "end": sorted_timeline[-1].timestamp.isoformat(),
                    "duration_hours": (sorted_timeline[-1].timestamp - sorted_timeline[0].timestamp).total_seconds() / 3600
                },
                "unique_symptoms": len(set(entry.symptom.lower() for entry in sorted_timeline))
            },
            "pattern_analysis": {
                "rapid_onset": rapid_onset_patterns,
                "severity_trends": severity_trends,
                "cyclical_patterns": cyclical_patterns,
                "symptom_clusters": symptom_clusters,
                "temporal_associations": temporal_associations,
                "emergency_indicators": emergency_indicators
            },
            "ai_analysis": ai_analysis,
            "risk_assessment": risk_assessment,
            "clinical_recommendations": recommendations,
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
    
    def _detect_rapid_onset(self, timeline: List[SymptomTimelineEntry]) -> List[Dict[str, Any]]:
        """Detect rapid onset patterns (multiple symptoms within short timeframe)"""
        patterns = []
        
        # Look for symptoms appearing within 1-hour windows
        for i in range(len(timeline)):
            rapid_onset_group = [timeline[i]]
            
            # Find symptoms within 1 hour of current symptom
            for j in range(i + 1, len(timeline)):
                time_diff = (timeline[j].timestamp - timeline[i].timestamp).total_seconds() / 3600
                if time_diff <= 1:
                    rapid_onset_group.append(timeline[j])
                elif time_diff > 1:
                    break
            
            # If 3 or more symptoms in 1 hour, it's a rapid onset pattern
            if len(rapid_onset_group) >= 3:
                severity_scores = [s.severity for s in rapid_onset_group if s.severity is not None]
                avg_severity = sum(severity_scores) / len(severity_scores) if severity_scores else None
                
                # Check for emergency keywords
                emergency_symptoms = [
                    s.symptom for s in rapid_onset_group 
                    if any(keyword in s.symptom.lower() for keyword in self.emergency_keywords)
                ]
                
                pattern = {
                    "type": "rapid_onset",
                    "symptom_count": len(rapid_onset_group),
                    "timeframe_minutes": int((rapid_onset_group[-1].timestamp - rapid_onset_group[0].timestamp).total_seconds() / 60),
                    "symptoms": [s.symptom for s in rapid_onset_group],
                    "average_severity": avg_severity,
                    "emergency_symptoms": emergency_symptoms,
                    "clinical_significance": self._assess_rapid_onset_significance(rapid_onset_group, emergency_symptoms),
                    "urgency_level": "high" if emergency_symptoms or (avg_severity and avg_severity >= 7) else "moderate"
                }
                
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_severity_trends(self, timeline: List[SymptomTimelineEntry]) -> List[SeverityTrend]:
        """Analyze severity trends for individual symptoms"""
        trends = []
        
        # Group by symptom
        symptom_groups = {}
        for entry in timeline:
            if entry.severity is not None:
                if entry.symptom.lower() not in symptom_groups:
                    symptom_groups[entry.symptom.lower()] = []
                symptom_groups[entry.symptom.lower()].append(entry)
        
        # Analyze trend for each symptom with multiple entries
        for symptom, entries in symptom_groups.items():
            if len(entries) >= 3:  # Need at least 3 points for trend analysis
                # Sort by timestamp
                entries.sort(key=lambda x: x.timestamp)
                
                # Calculate trend
                timestamps = [(e.timestamp - entries[0].timestamp).total_seconds() / 3600 for e in entries]
                severities = [e.severity for e in entries]
                
                # Simple linear regression for trend
                n = len(timestamps)
                sum_x = sum(timestamps)
                sum_y = sum(severities)
                sum_xy = sum(x * y for x, y in zip(timestamps, severities))
                sum_x2 = sum(x * x for x in timestamps)
                
                slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x) if (n * sum_x2 - sum_x * sum_x) != 0 else 0
                
                # Determine trend direction
                if abs(slope) < 0.1:
                    direction = "stable"
                elif slope > 0:
                    direction = "increasing"
                else:
                    direction = "decreasing"
                
                # Calculate correlation coefficient
                try:
                    correlation = statistics.correlation(timestamps, severities) if len(timestamps) > 1 else 0
                except:
                    correlation = 0
                
                # Assess clinical significance
                significance = self._assess_severity_trend_significance(symptom, direction, slope, severities)
                
                trend = SeverityTrend(
                    symptom=symptom,
                    trend_direction=direction,
                    slope=slope,
                    correlation_coefficient=correlation,
                    significance=significance
                )
                
                trends.append(trend)
        
        return trends
    
    def _detect_cyclical_patterns(self, timeline: List[SymptomTimelineEntry]) -> List[Dict[str, Any]]:
        """Detect cyclical/recurring symptom patterns"""
        patterns = []
        
        # Group symptoms by type
        symptom_occurrences = {}
        for entry in timeline:
            symptom_key = entry.symptom.lower()
            if symptom_key not in symptom_occurrences:
                symptom_occurrences[symptom_key] = []
            symptom_occurrences[symptom_key].append(entry)
        
        # Analyze patterns for symptoms with multiple occurrences
        for symptom, occurrences in symptom_occurrences.items():
            if len(occurrences) >= 3:
                # Sort by timestamp
                occurrences.sort(key=lambda x: x.timestamp)
                
                # Calculate intervals between occurrences
                intervals = []
                for i in range(1, len(occurrences)):
                    interval = (occurrences[i].timestamp - occurrences[i-1].timestamp).total_seconds() / 3600
                    intervals.append(interval)
                
                # Check for regular intervals (cyclical pattern)
                if len(intervals) >= 2:
                    avg_interval = sum(intervals) / len(intervals)
                    interval_variance = statistics.variance(intervals) if len(intervals) > 1 else 0
                    
                    # Consider it cyclical if intervals are relatively consistent
                    if interval_variance < (avg_interval * 0.5):  # Low variance relative to mean
                        pattern = {
                            "type": "cyclical",
                            "symptom": symptom,
                            "occurrence_count": len(occurrences),
                            "average_interval_hours": avg_interval,
                            "interval_variance": interval_variance,
                            "pattern_consistency": "high" if interval_variance < (avg_interval * 0.3) else "moderate",
                            "clinical_significance": self._assess_cyclical_significance(symptom, avg_interval, len(occurrences))
                        }
                        
                        patterns.append(pattern)
        
        return patterns
    
    def _identify_symptom_clusters(self, timeline: List[SymptomTimelineEntry]) -> List[SymptomCluster]:
        """Identify groups of symptoms that appear together"""
        clusters = []
        
        # Look for symptoms within 4-hour windows
        for i in range(len(timeline)):
            cluster_symptoms = [timeline[i].symptom]
            cluster_start = timeline[i].timestamp
            cluster_end = timeline[i].timestamp
            
            # Find symptoms within 4 hours
            for j in range(i + 1, len(timeline)):
                time_diff = (timeline[j].timestamp - timeline[i].timestamp).total_seconds() / 3600
                if time_diff <= 4:
                    if timeline[j].symptom not in cluster_symptoms:
                        cluster_symptoms.append(timeline[j].symptom)
                        cluster_end = timeline[j].timestamp
                else:
                    break
            
            # If cluster has 2+ different symptoms, analyze it
            if len(cluster_symptoms) >= 2:
                # Check if this cluster pattern repeats
                pattern_frequency = self._count_cluster_frequency(timeline, cluster_symptoms, 4)
                
                if pattern_frequency >= 2:  # Pattern appears at least twice
                    significance = self._assess_cluster_significance(cluster_symptoms)
                    
                    cluster = SymptomCluster(
                        symptoms=cluster_symptoms,
                        timeframe=(cluster_start, cluster_end),
                        frequency=pattern_frequency,
                        clinical_significance=significance
                    )
                    
                    clusters.append(cluster)
        
        return clusters
    
    def _find_temporal_associations(self, timeline: List[SymptomTimelineEntry]) -> List[Dict[str, Any]]:
        """Find temporal associations between different symptoms"""
        associations = []
        
        # Look for symptoms that consistently follow other symptoms
        symptom_pairs = {}
        
        for i in range(len(timeline) - 1):
            current_symptom = timeline[i].symptom.lower()
            
            # Look at symptoms within next 24 hours
            for j in range(i + 1, len(timeline)):
                time_diff = (timeline[j].timestamp - timeline[i].timestamp).total_seconds() / 3600
                if time_diff <= 24:
                    next_symptom = timeline[j].symptom.lower()
                    if current_symptom != next_symptom:
                        pair_key = f"{current_symptom} -> {next_symptom}"
                        if pair_key not in symptom_pairs:
                            symptom_pairs[pair_key] = []
                        symptom_pairs[pair_key].append(time_diff)
                else:
                    break
        
        # Analyze pairs with multiple occurrences
        for pair, time_diffs in symptom_pairs.items():
            if len(time_diffs) >= 2:
                avg_delay = sum(time_diffs) / len(time_diffs)
                consistency = 1 - (statistics.stdev(time_diffs) / avg_delay) if avg_delay > 0 else 0
                
                if consistency > 0.3:  # Reasonably consistent timing
                    association = {
                        "type": "temporal_association",
                        "symptom_pair": pair,
                        "occurrence_count": len(time_diffs),
                        "average_delay_hours": avg_delay,
                        "timing_consistency": consistency,
                        "clinical_relevance": self._assess_association_relevance(pair, avg_delay)
                    }
                    
                    associations.append(association)
        
        return associations
    
    def _detect_emergency_patterns(self, timeline: List[SymptomTimelineEntry]) -> List[Dict[str, Any]]:
        """Detect patterns that suggest emergency conditions"""
        emergency_patterns = []
        
        # Pattern 1: Rapid escalation to severe symptoms
        for i in range(len(timeline) - 1):
            if timeline[i].severity and timeline[i+1].severity:
                severity_increase = timeline[i+1].severity - timeline[i].severity
                time_diff = (timeline[i+1].timestamp - timeline[i].timestamp).total_seconds() / 3600
                
                # Rapid severe escalation
                if severity_increase >= 4 and time_diff <= 2:
                    emergency_patterns.append({
                        "type": "rapid_escalation",
                        "severity_increase": severity_increase,
                        "timeframe_hours": time_diff,
                        "symptoms": [timeline[i].symptom, timeline[i+1].symptom],
                        "urgency": "high",
                        "recommendation": "Immediate medical evaluation required"
                    })
        
        # Pattern 2: Emergency keyword combinations
        emergency_symptom_count = 0
        emergency_symptoms = []
        
        for entry in timeline:
            if any(keyword in entry.symptom.lower() for keyword in self.emergency_keywords):
                emergency_symptom_count += 1
                emergency_symptoms.append(entry.symptom)
        
        if emergency_symptom_count >= 2:
            emergency_patterns.append({
                "type": "emergency_symptom_cluster",
                "emergency_symptom_count": emergency_symptom_count,
                "emergency_symptoms": emergency_symptoms,
                "urgency": "critical",
                "recommendation": "Emergency medical attention required immediately"
            })
        
        return emergency_patterns
    
    def _calculate_comprehensive_risk(
        self,
        timeline: List[SymptomTimelineEntry],
        rapid_onset_patterns: List[Dict[str, Any]],
        severity_trends: List[SeverityTrend],
        emergency_indicators: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate comprehensive risk assessment based on all patterns"""
        risk_factors = []
        risk_score = 0
        
        # Emergency patterns contribute most to risk
        for pattern in emergency_indicators:
            if pattern.get("urgency") == "critical":
                risk_score += 40
                risk_factors.append("Critical emergency patterns detected")
            elif pattern.get("urgency") == "high":
                risk_score += 25
                risk_factors.append("High-urgency patterns detected")
        
        # Rapid onset patterns
        for pattern in rapid_onset_patterns:
            if pattern.get("urgency_level") == "high":
                risk_score += 20
                risk_factors.append("Rapid onset of multiple symptoms")
            else:
                risk_score += 10
                risk_factors.append("Moderate rapid onset pattern")
        
        # Severity trends
        worsening_trends = [t for t in severity_trends if t.trend_direction == "increasing"]
        if worsening_trends:
            risk_score += len(worsening_trends) * 5
            risk_factors.append(f"{len(worsening_trends)} worsening symptom trends")
        
        # Recent high severity
        recent_entries = [e for e in timeline[-5:] if e.severity is not None]
        if recent_entries:
            max_recent_severity = max(e.severity for e in recent_entries)
            if max_recent_severity >= 8:
                risk_score += 15
                risk_factors.append("Recent severe symptoms (8+/10)")
            elif max_recent_severity >= 6:
                risk_score += 8
                risk_factors.append("Recent moderate-severe symptoms (6-7/10)")
        
        # Determine risk level
        if risk_score >= 50:
            risk_level = "critical"
        elif risk_score >= 30:
            risk_level = "high"
        elif risk_score >= 15:
            risk_level = "moderate"
        else:
            risk_level = "low"
        
        return {
            "risk_level": risk_level,
            "risk_score": min(100, risk_score),  # Cap at 100
            "risk_factors": risk_factors,
            "immediate_attention_required": risk_score >= 30,
            "emergency_evaluation_recommended": risk_score >= 50
        }
    
    def _generate_timeline_recommendations(
        self,
        rapid_onset_patterns: List[Dict[str, Any]],
        severity_trends: List[SeverityTrend],
        cyclical_patterns: List[Dict[str, Any]],
        emergency_indicators: List[Dict[str, Any]],
        risk_assessment: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations based on timeline analysis"""
        recommendations = []
        
        # Emergency recommendations
        if emergency_indicators:
            recommendations.append({
                "category": "emergency",
                "action": "Seek immediate emergency medical attention",
                "priority": "critical",
                "timeline": "Immediately",
                "reasoning": "Emergency patterns detected in symptom timeline"
            })
        
        # Rapid onset recommendations
        if rapid_onset_patterns and not emergency_indicators:
            recommendations.append({
                "category": "urgent",
                "action": "Urgent medical evaluation recommended",
                "priority": "high",
                "timeline": "Within 2-4 hours",
                "reasoning": "Rapid onset of multiple symptoms requires prompt assessment"
            })
        
        # Worsening trend recommendations
        worsening_trends = [t for t in severity_trends if t.trend_direction == "increasing"]
        if worsening_trends and risk_assessment["risk_level"] in ["moderate", "high"]:
            recommendations.append({
                "category": "monitoring",
                "action": "Close monitoring and medical follow-up for worsening symptoms",
                "priority": "high",
                "timeline": "Within 24 hours",
                "reasoning": f"Worsening trends detected in {len(worsening_trends)} symptoms"
            })
        
        # Cyclical pattern recommendations
        if cyclical_patterns:
            recommendations.append({
                "category": "follow_up",
                "action": "Discuss recurring symptom patterns with healthcare provider",
                "priority": "medium",
                "timeline": "At next appointment",
                "reasoning": "Cyclical patterns may indicate underlying condition requiring management"
            })
        
        # General timeline recommendations
        recommendations.append({
            "category": "documentation",
            "action": "Continue detailed symptom tracking with timestamps",
            "priority": "medium",
            "timeline": "Ongoing",
            "reasoning": "Timeline data provides valuable clinical information"
        })
        
        return recommendations
    
    # Helper methods for significance assessment
    def _assess_rapid_onset_significance(self, symptoms: List[SymptomTimelineEntry], emergency_symptoms: List[str]) -> str:
        """Assess clinical significance of rapid onset pattern"""
        if emergency_symptoms:
            return "High clinical significance - emergency evaluation required"
        elif len(symptoms) >= 5:
            return "Moderate-high significance - urgent evaluation recommended"
        else:
            return "Moderate significance - medical evaluation advised"
    
    def _assess_severity_trend_significance(self, symptom: str, direction: str, slope: float, severities: List[int]) -> str:
        """Assess significance of severity trend"""
        max_severity = max(severities)
        
        if direction == "increasing" and max_severity >= 7:
            return "High significance - worsening severe symptom requires immediate attention"
        elif direction == "increasing" and abs(slope) > 1:
            return "Moderate-high significance - rapid worsening trend"
        elif direction == "decreasing":
            return "Positive trend - symptom improving"
        else:
            return "Monitor for changes"
    
    def _assess_cyclical_significance(self, symptom: str, interval_hours: float, occurrences: int) -> str:
        """Assess significance of cyclical pattern"""
        if interval_hours < 24 and occurrences >= 4:
            return "High significance - frequent recurring pattern may indicate acute condition"
        elif 24 <= interval_hours <= 168:  # Daily to weekly
            return "Moderate significance - regular pattern suggests systematic evaluation needed"
        else:
            return "Low-moderate significance - document pattern for healthcare provider"
    
    def _assess_cluster_significance(self, symptoms: List[str]) -> str:
        """Assess significance of symptom cluster"""
        # Check if symptoms are from related systems
        cardiovascular_count = sum(1 for s in symptoms if any(cv in s.lower() for cv in self.symptom_categories["cardiovascular"]))
        neurological_count = sum(1 for s in symptoms if any(neuro in s.lower() for neuro in self.symptom_categories["neurological"]))
        
        if cardiovascular_count >= 2:
            return "High significance - cardiovascular symptom cluster requires prompt evaluation"
        elif neurological_count >= 2:
            return "High significance - neurological symptom cluster requires prompt evaluation"
        else:
            return "Moderate significance - symptom cluster pattern noted"
    
    def _assess_association_relevance(self, pair: str, delay_hours: float) -> str:
        """Assess clinical relevance of symptom associations"""
        if delay_hours < 1:
            return "High relevance - immediate symptom progression"
        elif delay_hours < 6:
            return "Moderate relevance - short-term symptom development"
        else:
            return "Low-moderate relevance - document pattern"
    
    def _count_cluster_frequency(self, timeline: List[SymptomTimelineEntry], cluster_symptoms: List[str], window_hours: int) -> int:
        """Count how many times a symptom cluster pattern appears"""
        frequency = 0
        
        for i in range(len(timeline)):
            found_symptoms = set()
            
            # Look within window
            for j in range(i, len(timeline)):
                time_diff = (timeline[j].timestamp - timeline[i].timestamp).total_seconds() / 3600
                if time_diff <= window_hours:
                    if timeline[j].symptom in cluster_symptoms:
                        found_symptoms.add(timeline[j].symptom)
                else:
                    break
            
            # If found most symptoms in cluster, count it
            if len(found_symptoms) >= len(cluster_symptoms) * 0.8:
                frequency += 1
        
        return frequency
    
    def _create_empty_analysis(self) -> Dict[str, Any]:
        """Create empty analysis when no timeline data available"""
        return {
            "timeline_metadata": {
                "total_entries": 0,
                "date_range": None,
                "unique_symptoms": 0
            },
            "pattern_analysis": {
                "rapid_onset": [],
                "severity_trends": [],
                "cyclical_patterns": [],
                "symptom_clusters": [],
                "temporal_associations": [],
                "emergency_indicators": []
            },
            "ai_analysis": {"message": "No timeline data available"},
            "risk_assessment": {
                "risk_level": "unknown",
                "risk_score": 0,
                "risk_factors": [],
                "immediate_attention_required": False,
                "emergency_evaluation_recommended": False
            },
            "clinical_recommendations": [
                {
                    "category": "documentation",
                    "action": "Begin symptom timeline tracking",
                    "priority": "low",
                    "timeline": "Ongoing",
                    "reasoning": "Timeline data improves clinical assessment"
                }
            ],
            "analysis_timestamp": datetime.utcnow().isoformat()
        }


# Global instance
timeline_analyzer = SymptomTimelineAnalyzer()