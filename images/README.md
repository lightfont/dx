# Case Images — drop-in manifest

The engine renders an image automatically whenever a `cases.json` finding has an `imageUrl`
field. The `<img>` tag points to `images/<imageUrl>` (`index.html`, `mkFinding`). If a file is
missing it is hidden via `onerror` (no broken-image icon), so unreferenced/unfilled slots are
harmless.

**To add an image:** obtain an openly-licensed, clinically-verified image, save it in this
folder with the exact filename below, and it appears in the case automatically — no code change.

Naming convention: `case{NNN}_{modality}_{descriptor}.jpg`

## Expected files (14)

### case_001 — Epigastric pain / Inferior STEMI
- [ ] `case001_ecg_inferior_stemi.jpg` — basic `bi01`: 12-lead ECG (inferior STEMI)
- [ ] `case001_cxr_normal.jpg` — basic `bi08`: normal CXR
- [ ] `case001_angio_rca_occlusion.jpg` — advanced `ai01`: coronary angiogram, RCA occlusion
- [ ] `case001_echo_inferior_wall_motion.jpg` — advanced `ai02`: echo, inferior wall motion abnormality

### case_002 — Breathlessness / SCLC + paraneoplastic SIADH
- [ ] `case002_cxr_hilar_mass_effusion.jpg` — basic `bi01`: CXR, hilar mass + effusion
- [ ] `case002_sputum_cytology_sclc.jpg` — basic `bi09`: sputum cytology (SCLC)
- [ ] `case002_ct_chest_sclc_staging.jpg` — advanced `ai01`: CT chest, SCLC staging
- [ ] `case002_bronch_biopsy_sclc_histo.jpg` — advanced `ai02`: bronchoscopic biopsy histology (SCLC)
- [ ] `case002_mri_brain_mets.jpg` — advanced `ai03`: MRI brain, metastases

### case_003 — Headache / CVST
- [ ] `case003_ct_head_dense_sinus.jpg` — basic `bi02`: CT head, dense sinus sign
- [ ] `case003_lp_opening_pressure.jpg` — basic `bi07`: LP opening pressure
- [ ] `case003_mrv_ssinus_thrombosis.jpg` — advanced `ai01`: MRV, sagittal sinus thrombosis
- [ ] `case003_ctv_empty_delta.jpg` — advanced `ai02`: CTV, empty delta sign
- [ ] `case003_mri_parietal_venous_infarct.jpg` — advanced `ai03`: MRI, parietal venous infarct
