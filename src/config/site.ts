export const siteConfig = {
  name: 'ProcureESG',
  description: 'AI-assisted ESG procurement platform.',
  tenderStates: [
    'draft',
    'open_for_proposals',
    'closed',
    'under_review',
    'awarded',
    'withdrawn',
    'archived',
  ] as const,
  submissionStates: [
    'draft',
    'submitted',
    'withdrawn',
    'disqualified',
    'under_review',
    'awarded',
    'not_awarded',
  ] as const,
};

export type TenderState = (typeof siteConfig.tenderStates)[number];
export type SubmissionState = (typeof siteConfig.submissionStates)[number];
