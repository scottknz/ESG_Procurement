# AI Copilot Architecture (Jack & Jill Pattern)

The ESG Procurement Platform is an **AI-first application**. The buyer does not manually click through forms and buttons to complete tasks. Instead, they have a **persistent AI copilot** that lives in a chat panel on the left side of every buyer workspace screen and executes actions on their behalf.

## UI Layout Pattern

```
+----------------------------------+-------------------------------+
|  AI COPILOT CHAT                |  WORKSPACE TABS              |
|  (Left Panel - 30% width)       |  (Right Panel - 70% width)    |
|                                  |                               |
|  [Chat history with agent]      |  [Overview | Submissions |   |
|  User: "Review submissions"     |   Evaluate | Messages | ...]  |
|  Agent: "I see 5 submissions.   |                               |
|         2 are missing certs."   |  [Active tab content renders  |
|                                  |   here - forms, tables, etc.] |
|  [User input box]               |                               |
|  "> Ask me anything..."          |                               |
+----------------------------------+-------------------------------+
```

This is directly inspired by Jack & Jill AI recruitment platform, where Jack (the candidate-facing agent) and Jill (the recruiter-facing agent) maintain persistent conversational context while manipulating the workspace.

## Core Capabilities

The AI copilot must be able to:

### 1. Answer Questions (Read-only)
- "How many suppliers have submitted so far?"  
  → Agent queries `supplier_submissions` table and responds with count
- "What is the deadline for this tender?"  
  → Agent reads `tenders.submission_deadline` and formats the response
- "Which submission scored highest?"  
  → Agent calculates weighted scores from `evaluations` and returns ranked list
- "Show me all suppliers who didn't upload insurance certs"  
  → Agent queries custom questions in `submission_answers` and identifies gaps

### 2. Execute Actions (Write operations)
- "Draft a rejection email to Supplier ABC"  
  → Agent generates email draft, saves to `tender_messages` with status `Draft`, opens Messages tab
- "Edit the RFP to add TCFD compliance requirements"  
  → Agent updates `tenders.rfp_document_draft` (TipTap JSON), marks tender for republish, opens RFP Editor tab
- "Extend the deadline by 7 days"  
  → Agent updates `tenders.submission_deadline`, creates `tender_amendments` record, drafts notification email
- "Set this submission's review label to Follow Up"  
  → Agent updates `supplier_submissions.review_label_id`

### 3. Proactive Insights (Triggered alerts)
- Agent monitors tender state and proactively messages buyer:
  - "⚠️ Deadline is in 2 hours. You have 3 unscored submissions."  
  - "✅ All 5 submissions now have complete documentation."  
  - "🚨 Supplier XYZ just asked a clarification question. Review it in the Q&A tab."  

### 4. Multi-Step Workflows (Chain of actions)
- "Award the tender to Supplier ABC"  
  → Agent executes full award sequence:
    1. Updates `tenders.awarded_to_submission_id`
    2. Sets `supplier_submissions.status` to `Selected` for winner, `Not Selected` for others
    3. Generates audit PDF and ZIP archive
    4. Drafts award email and rejection emails
    5. Triggers Stripe 5% invoice
    6. Notifies buyer: "Award complete. Review emails in Messages tab before sending."  

## Technical Implementation

### Database: Copilot Session State

🔴 ABSOLUTE: Do NOT use the SQL shown in this file as the migration source.
The canonical schema for `buyer_copilot_sessions` is defined in `Instructions/Database_Schema.md` (Section 2a: AI Configurations).
Always refer to `Database_Schema.md` as the single source of truth for column definitions.
This section is for architectural context only.

### API Route: Streaming Chat with Function Calling

`api/ai/copilot/route.ts`

This route uses Gemini's **function calling** (or OpenAI's function calling) to allow the agent to execute actions.

```typescript
import { streamText, tool } from 'ai';
import { google } from '@ai-sdk/google';
import { z } from 'zod';

export async function POST(req: Request) {
  const { messages, tenderId, profileId } = await req.json();
  
  const result = await streamText({
    // 🔴 ABSOLUTE: Never hardcode the model name. Read the model from the `ai_model_config`
    // table in Supabase for the relevant use_case (e.g. 'copilot_chat', 'rfp_generation').
    // Example: const modelName = await getAIModelConfig('copilot_chat');
    model: google(modelName), // modelName loaded from ai_model_config table
    messages,
    tools: {
      getSubmissions: tool({
        description: 'Get all supplier submissions for this tender',
        parameters: z.object({ tenderId: z.string() }),
        execute: async ({ tenderId }) => {
          // Query Supabase for submissions
          return { submissions: [...] };
        }
      }),
      draftEmail: tool({
        description: 'Draft an email to suppliers',
        parameters: z.object({
          tenderId: z.string(),
          recipientOrgIds: z.array(z.string()),
          subject: z.string(),
          body: z.string()
        }),
        execute: async (params) => {
          // Insert into tender_messages with status Draft
          return { messageId: '...' };
        }
      }),
      updateRFP: tool({
        description: 'Edit the RFP document',
        parameters: z.object({
          tenderId: z.string(),
          sectionToEdit: z.string(),
          newContent: z.string()
        }),
        execute: async (params) => {
          // Update tenders.rfp_document_draft
          return { success: true };
        }
      }),
      // ... more tools for extend deadline, set labels, award tender, etc.
    }
  });
  
  return result.toDataStreamResponse();
}
```

### Frontend: Persistent Chat Panel Component

`src/components/copilot/BuyerCopilot.tsx`

This component renders on every buyer workspace page as a fixed left sidebar.

```typescript
'use client';

import { useChat } from 'ai/react';
import { useParams } from 'next/navigation';

export function BuyerCopilot() {
  const { tender_id } = useParams();
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/ai/copilot',
    body: { tenderId: tender_id },
    onFinish: (message) => {
      // If agent executed an action, potentially refresh the workspace tab
    }
  });
  
  return (
    <div className="fixed left-0 top-16 bottom-0 w-[30%] border-r bg-background">
      <div className="flex flex-col h-full">
        <div className="flex-1 overflow-y-auto p-4">
          {messages.map(m => (
            <div key={m.id} className={m.role === 'user' ? 'text-right' : 'text-left'}>
              <p>{m.content}</p>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="p-4 border-t">
          <input 
            value={input} 
            onChange={handleInputChange}
            placeholder="Ask me anything..."
            className="w-full"
          />
        </form>
      </div>
    </div>
  );
}
```

### Layout Integration

Update `src/app/(buyer)/layout.tsx` to include the copilot panel:

```typescript
import { BuyerCopilot } from '@/components/copilot/BuyerCopilot';

export default function BuyerLayout({ children }) {
  return (
    <div className="flex">
      <BuyerCopilot />
      <main className="ml-[30%] flex-1">{children}</main>
    </div>
  );
}
```

## Function Calling Tools (Complete List)

The AI copilot must have access to these server-side functions:

| Tool Name | Description | Parameters | Database Impact |
|-----------|-------------|------------|----------------|
| `getSubmissions` | Fetch all supplier submissions for tender | `tenderId` | Read from `supplier_submissions` |
| `getSubmissionById` | Get details of one submission | `submissionId` | Read from `supplier_submissions` + related tables |
| `draftEmail` | Create draft email in messages | `recipients, subject, body` | Insert `tender_messages` (status: Draft) |
| `updateRFP` | Edit RFP document | `tenderId, sectionPath, newContent` | Update `tenders.rfp_document_draft` |
| `extendDeadline` | Change submission deadline | `tenderId, newDeadline` | Update `tenders.submission_deadline` + `tender_amendments` |
| `setReviewLabel` | Triage submission | `submissionId, labelId` | Update `supplier_submissions.review_label_id` |
| `calculateScores` | Get ranked submissions | `tenderId` | Read `evaluations` + calculate weighted scores |
| `awardTender` | Full award workflow | `tenderId, winningSubmissionId` | Multi-table update (see award flow) |
| `answerQA` | Respond to supplier question | `clarificationId, answerText` | Update `tender_clarifications.answer_text` |
| `publishAmendment` | Publish RFP change | `tenderId, changeSummary` | Update `tenders.version` + insert `tender_amendments` |

## Context Awareness

The copilot must know:
- **Which tender** the buyer is currently viewing (from URL params)
- **Which tab** is active (Overview, Submissions, Evaluate, Messages)
- **Filters applied** (e.g., "Show only unscored submissions")
- **Recent actions** (e.g., buyer just opened Submission #5)

This context is passed in the `context` JSONB field and included in every API call to `/api/ai/copilot`.

## Security & Permissions

All copilot function calls must:
1. Verify the authenticated user has permission (buyer_admin can award, buyer_editor cannot)
2. Check the tender belongs to the user's organization
3. Validate state transitions (can't award a Draft tender)
4. Log every action to `audit_logs`

## Proactive Alerts (Server-Sent Events)

For the copilot to proactively notify the buyer (e.g., "Deadline in 2 hours"), use Server-Sent Events or a WebSocket connection.

Alternatively, use a polling approach where the copilot checks for alerts every 30 seconds and surfaces them in the chat.

---

This architecture transforms the platform from a traditional form-based SaaS tool into an AI-first copilot experience, where the buyer primarily interacts with the agent via natural language, and the agent manipulates the UI and database on their behalf.


---

# Supplier AI Copilot

Suppliers also have a persistent AI agent that assists them through the entire bid submission process. The supplier copilot uses the same left-panel chat interface (30% width) with workspace tabs on the right (70% width).

## Supplier Copilot Capabilities

### 1. Answer Questions (Read-only)
- "What is the submission deadline for this tender?"  
  → Agent reads `tenders.submission_deadline` and formats response
- "What documents do I need to upload?"  
  → Agent reads `tender_submission_config` and lists required attachments
- "How many custom questions are there?"  
  → Agent counts items in `tender_submission_config.custom_questions`
- "What are the evaluation criteria?"  
  → Agent reads `tender_criteria` and explains weighting
- "Has the buyer answered my clarification question yet?"  
  → Agent checks `tender_clarifications` for answers

### 2. Execute Actions (Write operations)
- "Draft an answer to question 5 about our carbon reduction methodology"  
  → Agent generates draft text, saves to `submission_answers` with status `Draft`
- "Ask the buyer: Do you require ISO 27001 or will ISO 9001 suffice?"  
  → Agent creates `tender_clarifications` record with supplier question
- "Upload my company's insurance certificate"  
  → Agent triggers file upload flow, stores in `submission_attachments`
- "Add John Smith as a team member with day rate £800"  
  → Agent inserts into `submission_team_profiles`
- "Set our total bid amount to £45,000"  
  → Agent updates `supplier_submissions.total_bid_amount`

### 3. Proactive Guidance (Triggered assistance)
- Agent monitors submission state and proactively guides supplier:
  - "⚠️ You have 3 mandatory questions unanswered. Let me help you draft responses."  
  - "✅ All required documents uploaded. Ready to submit?"  
  - "📋 The buyer just published an answer to your question about ISO standards."  
  - "⏰ Deadline is in 6 hours. Your submission is 80% complete."

### 4. Intelligent Form Completion (AI-assisted drafting)
- "Help me answer question 3 about our ESG track record"  
  → Agent reads the question context, checks supplier's `master_compliance_data`, and drafts a compliant response
- "Review my executive summary and suggest improvements"  
  → Agent reads `supplier_submissions.executive_summary`, applies NLP analysis, suggests edits
- "Generate a budget breakdown for this project"  
  → Agent creates structured `submission_budget_items` based on project scope

### 5. Pre-Submission Validation
- "Am I ready to submit?"  
  → Agent checks:
    - All mandatory questions answered
    - Required attachments uploaded
    - Total bid amount set
    - Executive summary written (if required)
    - Team profiles added (if required)
  → Returns checklist with missing items highlighted

## Technical Implementation

### Database: Supplier Copilot Session State

🔴 ABSOLUTE: Do NOT use the SQL shown in this file as the migration source.
The canonical schema for `supplier_copilot_sessions` is defined in `Instructions/Database_Schema.md` (Section 2a: AI Configurations).
Always refer to `Database_Schema.md` as the single source of truth for column definitions.
This section is for architectural context only.

### API Route: Supplier Copilot Chat

`api/ai/supplier-copilot/route.ts`

```typescript
import { streamText, tool } from 'ai';
import { google } from '@ai-sdk/google';
import { z } from 'zod';

export async function POST(req: Request) {
  const { messages, tenderId, supplierOrgId, profileId } = await req.json();
  
  const result = await streamText({
    // 🔴 ABSOLUTE: Never hardcode the model name. Read the model from the `ai_model_config`
    // table in Supabase for the relevant use_case (e.g. 'copilot_chat', 'rfp_generation').
    // Example: const modelName = await getAIModelConfig('copilot_chat');
    model: google(modelName), // modelName loaded from ai_model_config table
    messages,
    system: `You are an AI assistant helping a supplier complete their bid submission for a procurement tender. Be helpful, professional, and guide them through the process step-by-step.`,
    tools: {
      getTenderDetails: tool({
        description: 'Get tender requirements and deadline',
        parameters: z.object({ tenderId: z.string() }),
        execute: async ({ tenderId }) => {
          // Query tenders + tender_submission_config
          return { deadline, requirements, customQuestions };
        }
      }),
      draftAnswer: tool({
        description: 'Draft an answer to a custom question',
        parameters: z.object({
          questionId: z.string(),
          context: z.string()
        }),
        execute: async (params) => {
          // Generate draft using Gemini, save to submission_answers
          return { draftText };
        }
      }),
      askClarification: tool({
        description: 'Submit a question to the buyer',
        parameters: z.object({
          tenderId: z.string(),
          questionText: z.string()
        }),
        execute: async (params) => {
          // Insert into tender_clarifications
          return { clarificationId };
        }
      }),
      addTeamMember: tool({
        description: 'Add a team member to the bid',
        parameters: z.object({
          name: z.string(),
          roleTitle: z.string(),
          dayRate: z.number()
        }),
        execute: async (params) => {
          // Insert into submission_team_profiles
          return { success: true };
        }
      }),
      setBidAmount: tool({
        description: 'Set the total bid amount',
        parameters: z.object({
          amount: z.number()
        }),
        execute: async (params) => {
          // Update supplier_submissions.total_bid_amount
          return { success: true };
        }
      }),
      checkReadiness: tool({
        description: 'Check if submission is ready to submit',
        parameters: z.object({ submissionId: z.string() }),
        execute: async ({ submissionId }) => {
          // Validate all required fields
          return { ready: boolean, missingItems: [] };
        }
      }),
      // ... more tools
    }
  });
  
  return result.toDataStreamResponse();
}
```

### Frontend: Supplier Copilot Component

`src/components/copilot/SupplierCopilot.tsx`

```typescript
'use client';

import { useChat } from 'ai/react';
import { useParams } from 'next/navigation';

export function SupplierCopilot() {
  const { tender_id } = useParams();
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/ai/supplier-copilot',
    body: { tenderId: tender_id },
  });
  
  return (
    <div className="fixed left-0 top-16 bottom-0 w-[30%] border-r bg-background">
      <div className="flex flex-col h-full">
        <div className="p-4 border-b">
          <h2 className="font-semibold">Your AI Assistant</h2>
          <p className="text-sm text-muted-foreground">Ask me anything about this tender</p>
        </div>
        <div className="flex-1 overflow-y-auto p-4">
          {messages.map(m => (
            <div key={m.id} className={m.role === 'user' ? 'text-right' : 'text-left'}>
              <p>{m.content}</p>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="p-4 border-t">
          <input 
            value={input} 
            onChange={handleInputChange}
            placeholder="Ask me anything..."
            className="w-full"
          />
        </form>
      </div>
    </div>
  );
}
```

## Supplier Function Calling Tools (Complete List)

| Tool Name | Description | Parameters | Database Impact |
|-----------|-------------|------------|----------------|
| `getTenderDetails` | Fetch tender requirements | `tenderId` | Read from `tenders` + `tender_submission_config` |
| `getEvaluationCriteria` | Get scoring criteria | `tenderId` | Read from `tender_criteria` |
| `draftAnswer` | Generate answer to custom question | `questionId, context` | Insert/update `submission_answers` |
| `askClarification` | Submit question to buyer | `tenderId, questionText` | Insert `tender_clarifications` |
| `getClarifications` | Get Q&A history | `tenderId` | Read from `tender_clarifications` |
| `addTeamMember` | Add team profile | `name, role, dayRate` | Insert `submission_team_profiles` |
| `addBudgetItem` | Add budget line item | `category, amount` | Insert `submission_budget_items` |
| `setBidAmount` | Set total price | `amount` | Update `supplier_submissions.total_bid_amount` |
| `uploadDocument` | Trigger file upload | `documentType` | Insert `submission_attachments` after upload |
| `checkReadiness` | Validate submission completeness | `submissionId` | Read all submission tables |
| `submitBid` | Final submission | `submissionId` | Update `supplier_submissions.status` to Submitted |
| `reviewExecutiveSummary` | AI review of summary | `summaryText` | Read-only analysis |

## Context Awareness

The supplier copilot must know:
- **Which tender** the supplier is bidding on
- **Submission status** (Draft, percentage complete)
- **Active tab** (Overview, Questions, Team, Budget, Attachments, Review)
- **Missing requirements** (unanswered questions, missing docs)
- **Deadline proximity** (hours remaining)

## Proactive Onboarding

When a supplier first opens a tender, the copilot should proactively say:

> "👋 Welcome! I'm your AI assistant for this tender. I can help you understand the requirements, draft answers, and ensure your submission is complete. Let's start by reviewing what's required. Would you like me to walk you through the key sections?"

## Security & Permissions

All supplier copilot function calls must:
1. Verify the authenticated user belongs to the supplier organization
2. Check the tender is accessible (Published or Private with valid invitation/unlock)
3. Ensure submission is still in Draft status (can't edit after submission)
4. Validate all inputs before writing to database
5. Log actions to `audit_logs`

---

With both buyer and supplier copilots implemented, the platform becomes a true AI-first procurement experience where both sides of the transaction are supported by intelligent agents.
