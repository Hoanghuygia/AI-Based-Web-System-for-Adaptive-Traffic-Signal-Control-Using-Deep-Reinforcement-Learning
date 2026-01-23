import { useState, useCallback, useEffect } from 'react';
import { SettingsData, DEFAULT_SETTINGS } from '../types';

interface UseSettingsReturn {
    settings: SettingsData;
    initialSettings: SettingsData;
    isLoading: boolean;
    isSaving: boolean;
    error: string | null;
    updateSettings: <K extends keyof SettingsData>(
        section: K,
        data: Partial<SettingsData[K]>
    ) => void;
    saveSettings: () => Promise<void>;
    resetSettings: () => void;
    fetchSettings: () => Promise<void>;
}

export function useSettings(): UseSettingsReturn {
    const [settings, setSettings] = useState<SettingsData>(DEFAULT_SETTINGS);
    const [initialSettings, setInitialSettings] = useState<SettingsData>(DEFAULT_SETTINGS);
    const [isLoading, setIsLoading] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Fetch settings from API
    const fetchSettings = useCallback(async () => {
        setIsLoading(true);
        setError(null);

        try {
            // TODO: Replace with actual API call
            // const response = await fetch('/api/settings');
            // const data = await response.json();

            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 500));

            // For now, use default settings
            const fetchedSettings = DEFAULT_SETTINGS;

            setSettings(fetchedSettings);
            setInitialSettings(fetchedSettings);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to fetch settings');
        } finally {
            setIsLoading(false);
        }
    }, []);

    // Update settings section
    const updateSettings = useCallback(
        <K extends keyof SettingsData>(
            section: K,
            data: Partial<SettingsData[K]>
        ) => {
            setSettings(prev => ({
                ...prev,
                [section]: {
                    ...prev[section],
                    ...data,
                },
            }));
        },
        []
    );

    // Save settings to API
    const saveSettings = useCallback(async () => {
        setIsSaving(true);
        setError(null);

        try {
            // TODO: Replace with actual API call
            // const response = await fetch('/api/settings', {
            //   method: 'PUT',
            //   headers: { 'Content-Type': 'application/json' },
            //   body: JSON.stringify(settings),
            // });
            // if (!response.ok) throw new Error('Failed to save settings');

            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 1000));

            setInitialSettings(settings);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to save settings');
            throw err;
        } finally {
            setIsSaving(false);
        }
    }, [settings]);

    // Reset settings to initial values
    const resetSettings = useCallback(() => {
        setSettings(initialSettings);
        setError(null);
    }, [initialSettings]);

    // Fetch settings on mount
    useEffect(() => {
        fetchSettings();
    }, [fetchSettings]);

    return {
        settings,
        initialSettings,
        isLoading,
        isSaving,
        error,
        updateSettings,
        saveSettings,
        resetSettings,
        fetchSettings,
    };
}
