export interface User {
  uid: string
  email: string
  display_name: string
  avatar_url: string | null
  default_budget_id: string | null
  created_at: Date
}

export interface Budget {
  id: string
  name: string
  currency: string
  author_id: string
  member_ids: string[]
  created_at: Date
  updated_at: Date
}

export interface BudgetMember {
  id: string
  budget_id: string
  user_id: string
  role: 'owner' | 'editor' | 'viewer'
  joined_at: Date
  user?: User
}

export interface BudgetInvite {
  id: string
  budget_id: string
  invited_by: string
  code: string
  expires_at: Date
  used_by: string | null
  created_at: Date
}

export interface Category {
  id: string
  budget_id: string
  name: string
  icon_name: string
  color: string | null
  type: 'expense' | 'income'
  sort_order: number
  is_archived: boolean
}

export interface Transaction {
  id: string
  budget_id: string
  category_id: string
  user_id: string
  amount: number
  type: 'expense' | 'income'
  currency: string
  note: string | null
  occurred_at: Date
  created_at: Date
  category?: Category
  user?: User
}
