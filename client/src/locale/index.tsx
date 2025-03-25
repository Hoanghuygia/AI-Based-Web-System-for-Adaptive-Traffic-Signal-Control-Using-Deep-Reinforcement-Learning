import React, { FC } from "react";
import en_US from "./en-US";
import { MessageDescriptor, FormattedMessage, useIntl } from "react-intl";

export const localeConfig = {
  en_US: en_US,
};

type Id = keyof typeof en_US;

interface Props extends MessageDescriptor {
  id: Id;
}

export const LocaleFormatter: FC<Props> = ({ children, ...props }) => {
  return <FormattedMessage {...props} />;
};

type FormatMessageProps = (
  descriptor: MessageDescriptor,
  values?: Record<string, React.ReactNode>
) => string;

export const useLocale = () => {
  const { formatMessage: _formatMessage, ...rest } = useIntl();
  const formatMessage: FormatMessageProps = (descriptor, values) =>
    _formatMessage(descriptor, values);
  return {
    ...rest,
    formatMessage,
  };
};
