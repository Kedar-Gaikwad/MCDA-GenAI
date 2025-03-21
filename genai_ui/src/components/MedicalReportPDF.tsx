import React from 'react';
import { Document, Page, Text, View, StyleSheet } from '@react-pdf/renderer';

interface PatientInfo {
  NAME: string;
  SEX: string;
  AGE: string;
  DATE: string;
  'UHID.NO': string;
  'REF. By': string;
  OTHER: Record<string, string>;
}

interface MedicalReportData {
  patient_info: PatientInfo;
  findings: string[];
  comments: string[];
}

const styles = StyleSheet.create({
  page: {
    padding: 30,
  },
  header: {
    fontSize: 24,
    marginBottom: 20,
    textAlign: 'center',
  },
  section: {
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 18,
    marginBottom: 10,
    fontWeight: 'bold',
  },
  infoGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 15,
  },
  infoField: {
    width: '50%',
    marginBottom: 10,
  },
  label: {
    fontSize: 12,
    fontWeight: 'bold',
    marginBottom: 2,
  },
  value: {
    fontSize: 12,
    marginBottom: 5,
  },
  listItem: {
    marginBottom: 5,
    fontSize: 12,
  },
  customField: {
    width: '50%',
    marginBottom: 10,
  },
});

const MedicalReportPDF: React.FC<{ data: MedicalReportData }> = ({ data }) => {
  return (
    <Document>
      <Page size="A4" style={styles.page}>
        <Text style={styles.header}>Osciloist Medical Report</Text>

        {/* Patient Information Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Patient Information</Text>
          <View style={styles.infoGrid}>
            {Object.entries(data.patient_info)
              .filter(([key]) => key !== 'OTHER')
              .map(([key, value]) => (
                <View key={key} style={styles.infoField}>
                  <Text style={styles.label}>{key}:</Text>
                  <Text style={styles.value}>{value}</Text>
                </View>
              ))}
            
            {/* Custom fields from OTHER */}
            {Object.entries(data.patient_info.OTHER).map(([key, value]) => (
              <View key={key} style={styles.customField}>
                <Text style={styles.label}>{key}:</Text>
                <Text style={styles.value}>{value}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Findings Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Findings</Text>
          {data.findings.map((finding, index) => (
            <Text key={index} style={styles.listItem}>
              • {finding}
            </Text>
          ))}
        </View>

        {/* Comments Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Comments</Text>
          {data.comments.map((comment, index) => (
            <Text key={index} style={styles.listItem}>
              • {comment}
            </Text>
          ))}
        </View>
      </Page>
    </Document>
  );
};

export default MedicalReportPDF; 