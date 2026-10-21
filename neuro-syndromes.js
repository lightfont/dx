/* Dx/ Neuro Explorer — vascular syndrome table.
   STATUS: DRAFT — awaiting clinician validation (Dr Derek Soon). Edit here; the page reads it directly.

   Each syndrome:
     group      : 'Anterior circulation' | 'Posterior circulation' | 'Small vessel (lacunar)'
     bamford    : Oxford (Bamford) class — TACS / PACS / LACS / POCS
     views      : which schematic diagrams to draw ('axial', 'lateral', 'brainstem')
     regions    : regions to highlight per view.
                  axial   → aca | mca | pca | deep (basal ganglia + internal capsule) | thal
                  lateral → aca | mcaSup | mcaInf | pca
                  brainstem → 'midbrain:med' | 'midbrain:lat' | 'pons:med' | 'pons:lat' | 'medulla:med' | 'medulla:lat'
     bilateral  : true when both sides are involved (side toggle then has no effect)
     signs      : side  'contra' = opposite the lesion · 'ipsi' = same side · 'bilat' = both · 'none' = not lateralising
                  hemi  'dom' / 'nondom' = only shown for a dominant (left) / non-dominant (right) lesion
                  key   true = the discriminating sign
     absent     : signs characteristically ABSENT — as useful for localising as the positives
*/
window.NEURO_SYNDROMES = [
  {
    id: 'aca', name: 'Anterior cerebral artery (ACA)', vessel: 'ACA', group: 'Anterior circulation', bamford: 'PACS',
    territory: 'Medial frontal and parietal lobes, including the leg area of the motor and sensory cortex (paracentral lobule).',
    views: ['axial', 'lateral'], regions: { axial: ['aca'], lateral: ['aca'] },
    signs: [
      { side: 'contra', text: 'Weakness of the leg, worse than the arm; face largely spared', key: true },
      { side: 'contra', text: 'Sensory loss in the leg' },
      { side: 'none', text: 'Abulia — apathy, slowed or absent responses (medial frontal lobe)' },
      { side: 'none', text: 'Urinary incontinence' },
      { side: 'none', text: 'Grasp reflex and other primitive reflexes' },
      { side: 'none', hemi: 'dom', text: 'Transcortical motor aphasia — little spontaneous speech, repetition intact' }
    ],
    absent: ['Homonymous hemianopia', 'Prominent face and arm weakness'],
    discriminator: 'Leg weaker than arm. The motor homunculus puts the leg on the medial surface, which the ACA supplies.',
    imaging: 'Medial frontal/parietal infarct on CT or MRI DWI.',
    mimic: 'Parasagittal meningioma; bilateral ACA infarcts can mimic a cord lesion (paraparesis).'
  },
  {
    id: 'mca-stem', name: 'MCA stem (M1) occlusion', vessel: 'MCA', group: 'Anterior circulation', bamford: 'TACS',
    territory: 'Whole lateral hemisphere plus the deep lenticulostriate territory (basal ganglia and internal capsule).',
    views: ['axial', 'lateral'], regions: { axial: ['mca', 'deep'], lateral: ['mcaSup', 'mcaInf'] },
    signs: [
      { side: 'contra', text: 'Hemiparesis — face and arm worse than leg', key: true },
      { side: 'contra', text: 'Hemisensory loss — face and arm worse than leg' },
      { side: 'contra', text: 'Homonymous hemianopia (optic radiation)' },
      { side: 'ipsi', text: 'Eyes deviate toward the lesion (frontal eye field) — they look away from the weak side' },
      { side: 'none', hemi: 'dom', text: 'Global aphasia', key: true },
      { side: 'contra', hemi: 'nondom', text: 'Hemispatial neglect of the opposite side; anosognosia', key: true }
    ],
    absent: ['Crossed signs (cranial nerve on one side, limbs on the other)'],
    discriminator: 'All three TACS components: higher cortical dysfunction, homonymous hemianopia, and motor/sensory loss in two of face, arm and leg.',
    imaging: 'Non-contrast CT first to exclude haemorrhage (hyperdense MCA sign may be seen); CTA to confirm occlusion for thrombectomy.',
    mimic: "Intracerebral haemorrhage (needs CT); hypoglycaemia; Todd's paresis."
  },
  {
    id: 'mca-sup', name: 'MCA superior division', vessel: 'MCA', group: 'Anterior circulation', bamford: 'PACS',
    territory: 'Lateral frontal lobe and anterior parietal lobe, above the Sylvian fissure — includes face/arm motor cortex and Broca’s area.',
    views: ['axial', 'lateral'], regions: { axial: ['mca'], lateral: ['mcaSup'] },
    signs: [
      { side: 'contra', text: 'Weakness of face and arm; leg relatively spared', key: true },
      { side: 'contra', text: 'Sensory loss of face and arm' },
      { side: 'none', hemi: 'dom', text: "Broca's (expressive) aphasia — non-fluent, effortful; comprehension relatively preserved", key: true },
      { side: 'none', hemi: 'nondom', text: 'Expressive aprosodia — flat, unemotional speech' }
    ],
    absent: ['Visual field defect (usually)', 'Marked leg weakness'],
    discriminator: 'Face–arm weakness with a non-fluent aphasia (dominant side).',
    imaging: 'Frontal/anterior parietal cortical infarct above the Sylvian fissure.',
    mimic: 'Frontal tumour or abscess (subacute onset).'
  },
  {
    id: 'mca-inf', name: 'MCA inferior division', vessel: 'MCA', group: 'Anterior circulation', bamford: 'PACS',
    territory: 'Temporal lobe and inferior parietal lobe, below the Sylvian fissure — includes Wernicke’s area and Meyer’s loop.',
    views: ['axial', 'lateral'], regions: { axial: ['mca'], lateral: ['mcaInf'] },
    signs: [
      { side: 'contra', text: "Superior homonymous quadrantanopia ('pie in the sky') — Meyer's loop" },
      { side: 'none', hemi: 'dom', text: "Wernicke's (receptive) aphasia — fluent but meaningless speech, poor comprehension", key: true },
      { side: 'contra', hemi: 'nondom', text: 'Hemispatial neglect; anosognosia; dressing and constructional apraxia', key: true }
    ],
    absent: ['Limb weakness (little or none)'],
    discriminator: 'Language or neglect deficit WITHOUT weakness — the patient who is "just confused".',
    imaging: 'Temporal/inferior parietal infarct below the Sylvian fissure.',
    mimic: 'Delirium or a psychiatric presentation — the classic missed stroke.'
  },
  {
    id: 'pca', name: 'Posterior cerebral artery (PCA)', vessel: 'PCA', group: 'Posterior circulation', bamford: 'POCS',
    territory: 'Occipital lobe, inferior temporal lobe and (via perforators) the thalamus.',
    views: ['axial', 'lateral'], regions: { axial: ['pca'], lateral: ['pca'] },
    signs: [
      { side: 'contra', text: 'Homonymous hemianopia with macular sparing', key: true },
      { side: 'contra', text: 'Hemisensory loss — if thalamic perforators are involved' },
      { side: 'none', hemi: 'dom', text: 'Alexia without agraphia — if the splenium of the corpus callosum is involved' },
      { side: 'none', hemi: 'nondom', text: 'Topographical disorientation; visual neglect' },
      { side: 'none', text: 'Visual hallucinations or agitation may occur' }
    ],
    absent: ['Limb weakness (usually)'],
    discriminator: 'An isolated field defect with macular sparing — patients often do not notice it themselves.',
    imaging: 'Occipital infarct; MRI DWI is more sensitive than CT for posterior circulation strokes.',
    mimic: 'Migraine with aura; occipital mass.'
  },
  {
    id: 'lacs-motor', name: 'Lacunar — pure motor', vessel: 'Lenticulostriate', group: 'Small vessel (lacunar)', bamford: 'LACS',
    territory: 'Posterior limb of the internal capsule (or ventral pons), supplied by small penetrating arteries.',
    views: ['axial'], regions: { axial: ['deep'] },
    signs: [
      { side: 'contra', text: 'Weakness of face, arm and leg equally (or two of the three)', key: true }
    ],
    absent: ['Sensory loss', 'Visual field defect', 'Aphasia or neglect', 'Drowsiness'],
    discriminator: 'Dense weakness with NO cortical signs. The fibres are packed tightly in the capsule, so a tiny lesion hits face, arm and leg together.',
    imaging: 'Small (<15 mm) deep infarct; CT is often normal early — MRI DWI.',
    mimic: 'Small deep haemorrhage (CT needed).'
  },
  {
    id: 'lacs-sensory', name: 'Lacunar — pure sensory', vessel: 'Thalamoperforators (PCA)', group: 'Small vessel (lacunar)', bamford: 'LACS',
    territory: 'Ventral posterolateral (VPL) nucleus of the thalamus.',
    views: ['axial'], regions: { axial: ['thal'] },
    signs: [
      { side: 'contra', text: 'Numbness of face, arm and leg (hemisensory loss)', key: true },
      { side: 'contra', text: 'Later: central post-stroke pain (Dejerine–Roussy)' }
    ],
    absent: ['Weakness', 'Visual field defect', 'Aphasia or neglect'],
    discriminator: 'Hemisensory loss splitting exactly at the midline, with no weakness.',
    imaging: 'Small thalamic infarct; MRI DWI.',
    mimic: 'Sensory seizure; functional sensory loss.'
  },
  {
    id: 'weber', name: "Weber's syndrome (midbrain)", vessel: 'Paramedian branches of PCA / top of basilar', group: 'Posterior circulation', bamford: 'POCS',
    territory: 'Ventromedial midbrain — cerebral peduncle and the CN III fascicle.',
    views: ['brainstem'], regions: { brainstem: ['midbrain:med'] },
    signs: [
      { side: 'ipsi', text: 'Oculomotor (CN III) palsy — ptosis, eye down and out, dilated pupil', key: true },
      { side: 'contra', text: 'Hemiparesis including the face (cerebral peduncle)', key: true }
    ],
    absent: ['Reduced consciousness (if present, think uncal herniation)'],
    discriminator: 'Crossed signs: cranial nerve III on the side of the lesion, limbs on the other.',
    imaging: 'MRI brainstem (CT poorly sensitive in the posterior fossa).',
    mimic: 'Uncal herniation — also III palsy with hemiparesis, but with falling GCS.'
  },
  {
    id: 'medial-pons', name: 'Medial pontine syndrome', vessel: 'Paramedian branches of basilar', group: 'Posterior circulation', bamford: 'POCS',
    territory: 'Medial pons — corticospinal tract, medial lemniscus and CN VI fascicle.',
    views: ['brainstem'], regions: { brainstem: ['pons:med'] },
    signs: [
      { side: 'contra', text: 'Hemiparesis (corticospinal tract)', key: true },
      { side: 'contra', text: 'Loss of vibration and proprioception (medial lemniscus)' },
      { side: 'ipsi', text: 'Abducens (CN VI) palsy — eye fails to abduct', key: true }
    ],
    absent: ['Pain and temperature loss (spinothalamic tract is lateral)'],
    discriminator: 'Crossed signs: CN VI on the side of the lesion, hemiparesis on the other.',
    imaging: 'MRI brainstem with DWI.',
    mimic: 'Demyelination (MS) in a young patient.'
  },
  {
    id: 'lateral-pons', name: 'Lateral pontine syndrome (AICA)', vessel: 'AICA', group: 'Posterior circulation', bamford: 'POCS',
    territory: 'Lateral pons and middle cerebellar peduncle; labyrinthine artery to the inner ear.',
    views: ['brainstem'], regions: { brainstem: ['pons:lat'] },
    signs: [
      { side: 'ipsi', text: 'Facial weakness — whole face, lower motor neuron pattern (CN VII nucleus)', key: true },
      { side: 'ipsi', text: 'Hearing loss and tinnitus (cochlear nucleus / labyrinthine artery)', key: true },
      { side: 'ipsi', text: 'Loss of pain and temperature on the face (spinal trigeminal nucleus)' },
      { side: 'contra', text: 'Loss of pain and temperature on the body (spinothalamic tract)' },
      { side: 'ipsi', text: 'Limb ataxia (middle cerebellar peduncle)' },
      { side: 'ipsi', text: "Horner's syndrome (descending sympathetic fibres)" },
      { side: 'none', text: 'Vertigo, nausea, nystagmus (vestibular nuclei)' }
    ],
    absent: ['Limb weakness'],
    discriminator: 'Like Wallenberg, but with facial palsy and hearing loss.',
    imaging: 'MRI brainstem with DWI.',
    mimic: 'Vestibular neuritis or labyrinthitis (but those have no crossed sensory signs).'
  },
  {
    id: 'locked-in', name: 'Basilar artery — locked-in syndrome', vessel: 'Basilar', group: 'Posterior circulation', bamford: 'POCS',
    territory: 'Bilateral ventral pons — both corticospinal and corticobulbar tracts.',
    views: ['brainstem'], regions: { brainstem: ['pons:med'] }, bilateral: true,
    signs: [
      { side: 'bilat', text: 'Quadriplegia', key: true },
      { side: 'bilat', text: 'Anarthria and inability to swallow (corticobulbar tracts)' },
      { side: 'bilat', text: 'Loss of horizontal eye movements' },
      { side: 'none', text: 'Consciousness, vertical eye movements and blinking PRESERVED', key: true }
    ],
    absent: ['Loss of awareness'],
    discriminator: 'Looks like coma but is not — ask the patient to look up and blink.',
    imaging: 'CTA/MRA for basilar occlusion — a thrombectomy emergency.',
    mimic: 'Coma; severe Guillain–Barré.'
  },
  {
    id: 'wallenberg', name: 'Lateral medullary (Wallenberg)', vessel: 'PICA or vertebral', group: 'Posterior circulation', bamford: 'POCS',
    territory: 'Lateral medulla and inferior cerebellar peduncle.',
    views: ['brainstem'], regions: { brainstem: ['medulla:lat'] },
    signs: [
      { side: 'ipsi', text: 'Loss of pain and temperature on the face (spinal trigeminal nucleus)', key: true },
      { side: 'contra', text: 'Loss of pain and temperature on the body (spinothalamic tract)', key: true },
      { side: 'ipsi', text: "Horner's syndrome — ptosis, miosis, anhidrosis (descending sympathetic fibres)" },
      { side: 'ipsi', text: 'Limb ataxia (inferior cerebellar peduncle)' },
      { side: 'ipsi', text: 'Dysphagia, hoarseness, reduced gag (nucleus ambiguus)' },
      { side: 'none', text: 'Vertigo, nausea, nystagmus (vestibular nuclei)' }
    ],
    absent: ['Limb weakness (corticospinal tract is medial)'],
    discriminator: 'Crossed sensory loss: pain/temperature lost on the face on one side and the body on the other.',
    imaging: 'MRI with DWI (CT usually normal); consider vertebral dissection in the young.',
    mimic: 'Peripheral vertigo — use HINTS.'
  },
  {
    id: 'medial-medulla', name: 'Medial medullary (Dejerine)', vessel: 'Anterior spinal / vertebral', group: 'Posterior circulation', bamford: 'POCS',
    territory: 'Medial medulla — pyramid, medial lemniscus and CN XII.',
    views: ['brainstem'], regions: { brainstem: ['medulla:med'] },
    signs: [
      { side: 'contra', text: 'Hemiparesis sparing the face (pyramid)', key: true },
      { side: 'contra', text: 'Loss of vibration and proprioception (medial lemniscus)' },
      { side: 'ipsi', text: 'Tongue weakness — tongue deviates toward the lesion (CN XII)', key: true }
    ],
    absent: ['Pain and temperature loss', 'Facial weakness'],
    discriminator: 'Tongue deviates to one side, the limbs are weak on the other.',
    imaging: 'MRI brainstem with DWI.',
    mimic: 'Motor neuron disease (but that is bilateral and progressive).'
  }
];
