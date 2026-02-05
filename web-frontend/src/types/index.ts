export interface User {
  id: number;
  username: string;
}

export interface AuthResponse {
  token: string;
  user_id: number;
  username: string;
}

export interface Equipment {
  id: number;
  equipment_name: string;
  equipment_type: string;
  flowrate: number;
  pressure: number;
  temperature: number;
}

export interface DatasetListItem {
  id: number;
  name: string;
  uploaded_at: string;
  equipment_count: number;
}

export interface Dataset {
  id: number;
  name: string;
  uploaded_at: string;
  file: string;
  equipment: Equipment[];
}

export interface Summary {
  total_count: number;
  avg_flowrate: number;
  avg_pressure: number;
  avg_temperature: number;
  type_distribution: Record<string, number>;
}
