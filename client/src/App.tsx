import './App.css';
import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter } from 'react-router-dom';
import { Provider, useSelector } from 'react-redux';
import { store, RootState } from './stores';
import { ConfigProvider } from 'antd';
// import enUS from 'antd/es/calendar/locale/en_US';
import enUS from 'antd/es/locale/en_US'
import viVN from 'antd/es/locale/vi_VN'
import { IntlProvider } from 'react-intl';
import { localeConfig } from './locale';

export type Locale = 'en_US' | 'vi_VN';

const queryClient = new QueryClient();

function App() {

    const locale = useSelector((state: RootState) => state.user.locale);

    const getAntdLocale = () => {
        if (locale === 'en_US') {
            return enUS;
        }
        else{
            return viVN;
        }
    }
    
    return (
        <Provider store={store}>
            <QueryClientProvider client={queryClient}>
                <ConfigProvider locale={getAntdLocale()} componentSize='middle'>
                    <IntlProvider locale={locale.split('_')[0]} messages={localeConfig[locale]}>
                    <BrowserRouter>
                        {/* Your routes */}
                    </BrowserRouter>
                    </IntlProvider>
                </ConfigProvider>
            </QueryClientProvider>
        </Provider>
    );
}

export default App;
