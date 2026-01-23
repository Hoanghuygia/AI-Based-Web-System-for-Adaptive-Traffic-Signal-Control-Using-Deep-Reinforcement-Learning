export interface AccountSettingsData {
  email: string;
  phoneNumber: string;
  language: string;
}

export interface NotificationSettingsData {
  emailNotifications: boolean;
  trafficAlerts: boolean;
  systemNotifications: boolean;
  weeklyReport: boolean;
}

export interface SystemPreferencesData {
  updateFrequency: number;
  maxCongestionThreshold: number;
  enableAutoOptimization: boolean;
}

export interface DisplaySettingsData {
  theme: string;
  dateFormat: string;
  timeFormat: string;
}

export interface SecuritySettingsData {
  twoFactorAuth: boolean;
  sessionTimeout: number;
}

export interface DataSettingsData {
  dataRetention: number;
  enableDataExport: boolean;
  autoBackup: boolean;
}

export interface APISettingsData {
  enableAPIAccess: boolean;
  apiRateLimit: number;
}

export interface SettingsData {
  account: AccountSettingsData;
  notifications: NotificationSettingsData;
  systemPreferences: SystemPreferencesData;
  display: DisplaySettingsData;
  security: SecuritySettingsData;
  data: DataSettingsData;
  api: APISettingsData;
}

export const DEFAULT_SETTINGS: SettingsData = {
  account: {
    email: 'admin@traffic-system.local',
    phoneNumber: '+84 912 345 678',
    language: 'English',
  },
  notifications: {
    emailNotifications: true,
    trafficAlerts: true,
    systemNotifications: true,
    weeklyReport: true,
  },
  systemPreferences: {
    updateFrequency: 5,
    maxCongestionThreshold: 80,
    enableAutoOptimization: true,
  },
  display: {
    theme: 'Light',
    dateFormat: 'DD/MM/YYYY',
    timeFormat: '24 Hour',
  },
  security: {
    twoFactorAuth: false,
    sessionTimeout: 30,
  },
  data: {
    dataRetention: 90,
    enableDataExport: true,
    autoBackup: true,
  },
  api: {
    enableAPIAccess: true,
    apiRateLimit: 1000,
  },
};
