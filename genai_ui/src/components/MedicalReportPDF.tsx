import React from 'react';
import { Document, Page, Text, View, StyleSheet, Image } from '@react-pdf/renderer';

interface PatientInfo {
  NAME: string;
  SEX: string;
  AGE: string;
  DATE: string;
  'UHID.NO': string;
  'REF. By': string;
  'REF.By': string;
  EXAMINATION?: string;
  OTHER: Record<string, string>;
}

interface MedicalReportData {
  patient_info: PatientInfo;
  findings: string[];
  FINDINGS?: string[];
  comments: string[];
  Comments?: string[];
}

const styles = StyleSheet.create({
  page: {
    padding: 30,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
    justifyContent: 'flex-start',
  },
  logo: {
    width: 130,
    height: 192,
    marginRight: 20,
  },
  title: {
    fontSize: 24,
    textAlign: 'left',
    marginBottom: 10,
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
  // Normalize the data to handle case differences
  const normalizedData = {
    ...data,
    findings: data.FINDINGS || data.findings || [],
    comments: data.Comments || data.comments || []
  };

  return (
    <Document>
      <Page size="A4" style={styles.page}>
        <View style={styles.header}>
          <Image src="/LogoOSCILO.png" style={styles.logo} />
          <Text style={styles.title}>Osciloist Medical Report</Text>
        </View>

        {/* Patient Information Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Patient Information</Text>
          <View style={styles.infoGrid}>
            {Object.entries(normalizedData.patient_info)
              .filter(([key]) => key !== 'OTHER' && key !== 'REF.By')
              .map(([key, value]) => (
                <View key={key} style={styles.infoField}>
                  <Text style={styles.label}>{key}:</Text>
                  <Text style={styles.value}>{value}</Text>
                </View>
              ))}
            
            {/* Custom fields from OTHER */}
            {Object.entries(normalizedData.patient_info.OTHER).map(([key, value]) => (
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
          {normalizedData.findings.map((finding, index) => (
            <Text key={index} style={styles.listItem}>
              • {finding}
            </Text>
          ))}
        </View>

        {/* Comments Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Comments</Text>
          {normalizedData.comments.map((comment, index) => (
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