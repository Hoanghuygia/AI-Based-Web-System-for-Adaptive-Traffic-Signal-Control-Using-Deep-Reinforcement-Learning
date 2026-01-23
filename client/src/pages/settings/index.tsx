import AccountSettings from "./components/AccountSettings";
import NotificationSettings from "./components/NotificationSettings";
import SystemPreferences from "./components/SystemPreferences";
import DisplaySettings from "./components/DisplaySettings";
import SecuritySettings from "./components/SecuritySettings";
import DataSettings from "./components/DataSettings";
import APISettings from "./components/APISettings";
import { useState } from "react";
import { Button, Spin, Alert } from "antd";
import {
    EditOutlined,
    SaveOutlined,
    LoadingOutlined,
} from "@ant-design/icons";
import { useSettings } from "./hooks/useSettings";

export default function Settings() {
    const {
        settings,
        isLoading,
        isSaving,
        error,
        updateSettings,
        saveSettings,
        resetSettings,
    } = useSettings();

    const [isEdit, setIsEdit] = useState(false);
    const [saveMessage, setSaveMessage] = useState("");

    const handleSave = async () => {
        try {
            await saveSettings();
            setSaveMessage("Settings saved successfully!");
            setIsEdit(false);
            setTimeout(() => setSaveMessage(""), 3000);
        } catch (err) {
            setSaveMessage("");
        }
    };

    const handleCancel = () => {
        resetSettings();
        setIsEdit(false);
        setSaveMessage("");
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Spin size="large" indicator={<LoadingOutlined style={{ fontSize: 48 }} spin />} />
            </div>
        );
    }

    return (
        <div
            id="setting-page"
            className="bg-white relative"
        >
            {error && (
                <Alert
                    message="Error"
                    description={error}
                    type="error"
                    closable
                    className="mb-6"
                />
            )}

            {saveMessage && (
                <Alert
                    message={saveMessage}
                    type="success"
                    closable
                    className="mb-6"
                />
            )}

            {/* Account settings */}
            <AccountSettings
                disabled={!isEdit}
                data={settings.account}
                onChange={(data) => updateSettings('account', data)}
            />
            <NotificationSettings
                disabled={!isEdit}
                data={settings.notifications}
                onChange={(data) => updateSettings('notifications', data)}
            />
            <SystemPreferences
                disabled={!isEdit}
                data={settings.systemPreferences}
                onChange={(data) => updateSettings('systemPreferences', data)}
            />
            <DisplaySettings
                disabled={!isEdit}
                data={settings.display}
                onChange={(data) => updateSettings('display', data)}
            />
            <SecuritySettings
                disabled={!isEdit}
                data={settings.security}
                onChange={(data) => updateSettings('security', data)}
            />
            <DataSettings
                disabled={!isEdit}
                data={settings.data}
                onChange={(data) => updateSettings('data', data)}
            />
            <APISettings
                disabled={!isEdit}
                data={settings.api}
                onChange={(data) => updateSettings('api', data)}
            />

            {/* Bottom action buttons */}
            <div className="flex justify-end mt-6 gap-2">
                {isEdit ? (
                    <>
                        <Button
                            onClick={handleCancel}
                            disabled={isSaving}
                            type="default"
                            className="h-12 w-24"
                        >
                            Cancel
                        </Button>
                        <Button
                            onClick={handleSave}
                            loading={isSaving}
                            type="primary"
                            className="!bg-purple-400 hover:!bg-purple-500 !border-purple-400 h-12"
                        >
                            <SaveOutlined />
                            Save Changes
                        </Button>
                    </>
                ) : (
                    <Button
                        onClick={() => setIsEdit(true)}
                        type="primary"
                        size="large"
                        className="!bg-purple-400 hover:!bg-purple-500 !border-purple-400 h-12"
                    >
                        <EditOutlined />
                        Edit Settings
                    </Button>
                )}
            </div>
        </div>
    );
}
