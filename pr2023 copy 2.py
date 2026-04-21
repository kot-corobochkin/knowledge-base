 public function prepareSearchReportData($found, $contrType, $params, $allGetValues){

        $company = Company::getInstance();
        $person = Person::getInstance();
        $ip = IndividualProprietor::getInstance();
        $contrId = $params['id'];

        $formatId = $params['format_id'];
        if (isset($checkContractorReports['extra']['limit'])) {
            $arrayCount = $found['found']['total_count'] = $checkContractorReports['extra']['limit'];
            $found['found']['data'] = array_slice($found['found']['data'], 0, $arrayCount);
        } else {
            $arrayCount = count($found['found']['data']);
        }


        if ($contrType == 'company') {
            $elementsCount = 1000;
            $iterationsCount = ceil($arrayCount / $elementsCount);
            if (!empty($found['found']['data'][0])) {
                $tmp = [];
                foreach ($found['found']['data'] as $row) {
                    $tmp[$row['id']]['id'] = $row['id'];
                }
                $found['found']['data'] = $tmp;
                unset($tmp);
            }
            for ($i = 1; $i <= $iterationsCount; $i++) {
                $offset = ($i > 1) ? $elementsCount * ($i - 1) : 0;
                $slice = array_slice($found['found']['data'], $offset, $elementsCount, true);

                $companies = $company->loadByIds(array_keys($slice));
                $directors = $company->director->loadByCompanyIds(array_keys($slice));
                $proceeds = $company->finBalance->getLastProceedsByIds(array_keys($slice));
                $contact = $company->contact->loadDataByCompanyIds(array_keys($slice));

                $register_address = $company->addressGar->loadByCompanyIds(array_keys($slice));
                # доп. информация по: телефон, e-mail, сайт
                $extraData = $company->companyExtraData->getExtraDataByCompanyIds(array_keys($slice));
                $finInfoYears = [2018, 2019, 2020, 2021, 2022, 2023, 2024];
                foreach ($companies as $key => $contr) {
                    $emailsData = $company->contacts->getEmailByCompanyId($key);
                    $siteData = $company->contacts->getSiteByCompanyId($key);
                    $found['found']['data'][$key] = $contr;

                    // Получение информации о директоре
                    if (!empty($directors[$key])) {
                        $found['found']['data'][$key]['directors'][0] = $directors[$key];
                    }

                    $finInfo = $company->financialInfo->loadByCompanyId($key, [3, 2, 1], 0, $finInfoYears);
                    // Получение информации по выручке компании
                    if (!empty($finInfo)) {
                        if (!empty($finInfo[Importer::BALANCES_LAST_YEAR]['2']['i_21103'])) {
                            $found['found']['data'][$key]['proceeds'] = $finInfo[Importer::BALANCES_LAST_YEAR]['2']['i_21103'];
                        }
                    }

                    $tmpBalaceData = [];
                    $reportFileString = [];
                    foreach ($finInfoYears as $infoYear) {
                        if (empty($finInfo) || empty($finInfo[$infoYear][2]) || empty($finInfo[$infoYear][2]['i_21203']) || empty($finInfo[$infoYear][2]['i_21103'])) {
                            $tmpBalaceData[$infoYear] = [
                                'i_13003' => '',
                                'i_21103' => '',
                                '2100' => '',
                                'rent' => '',
                            ];
                        } else {
                            $tmpBalaceData[$infoYear]['i_13003'] = $finInfo[$infoYear][1]['i_13003']; // Чистые активы
                            $tmpBalaceData[$infoYear]['i_21103'] = $finInfo[$infoYear][2]['i_21103']; // Выручка
                            $tmpBalaceData[$infoYear]['2100'] = $finInfo[$infoYear][2]['i_21103'] - $finInfo[$infoYear][2]['i_21203']; // Прибыль (убыток) от продажи
                            $rent = ($tmpBalaceData[$infoYear]['2100'] / $finInfo[$infoYear][2]['i_21203']) * 100; // Рентабельность затрат
                            $tmpBalaceData[$infoYear]['rent'] = number_format($rent, 2, ',', '');
                        }
                    }
                    foreach (['i_13003', 'i_21103', '2100', 'rent'] as $code) {
                        foreach ($tmpBalaceData as $year => $balance) {
                            if ($code != 'rent' && is_int($balance[$code])) {
                                $balance[$code] = number_format($balance[$code], 0, '.', ' ');
                            }
                            $reportFileString[$year . '_' . $code] = $balance[$code];
                        }
                    }
                    $found['found']['data'][$key]['balance'] = $reportFileString;

                    // адрес регистрации
                    if (!empty($register_address[$key])) {
                        $found['found']['data'][$key]['register_address'] = ['text' => $register_address[$key]['unparsed']];
                    } else {
                        $found['found']['data'][$key]['register_address'] = ['text' => ''];
                    }

                    // email's
                    if (!empty($contact[$key]['email']) || !empty($extraData[$key]['email']) || !empty($emailsData)) {
                        $emails = [];
                        if (!empty($contact[$key]['email'])) {
                            $emails = $contact[$key]['email'];
                        }
                        if (!empty($extraData[$key]['email'])) {
                            $emails = array_merge($emails, $extraData[$key]['email']);
                        }
                        if (!empty($emailsData)) {
                            foreach ($emailsData as $emailData) {
                                array_push($emails, strtolower($emailData['email']));
                            }
                        }
                        $found['found']['data'][$key]['email'] = implode(", ", $emails);
                    }

                    // site's
                    if (!empty($contact[$key]['site']) || !empty($extraData[$key]['website']) || !empty($siteData)) {
                        $sites = [];
                        if (!empty($contact[$key]['site'])) {
                            $sites = $contact[$key]['site'];
                        }
                        if (!empty($extraData[$key]['website'])) {
                            $sites = array_merge($sites, $extraData[$key]['website']);
                        }
                        if (!empty($siteData)) {
                            $sData = [];
                            foreach ($siteData as $s) {
                                $sData[] = $s['site'];
                            }
                            $sites = array_merge($sites, $sData);
                        }
                        $found['found']['data'][$key]['site'] = implode(", ", $sites);
                    }

                    // телефоны
                    $allPhones = $company->contacts->loadPhonesByCompanyIds([$key]);
                    $companyPhones = [];
                    if (!empty($allPhones)) {
                        foreach ($allPhones as $ph) {
                            if ($ph['company_id'] == $key) {
                                $tmp = $ph['phone_number'];
                                if ($ph['type'] == 2) $tmp .= " (факс)";
                                $tmp = trim($tmp);
                                if ($tmp) {
                                    $companyPhones[] = $tmp;
                                }
                            }
                        }
                    }
                    $found['found']['data'][$key]['contact'] = (!empty($companyPhones)) ? implode(", ", $companyPhones) : '';

                    $number_staff = 0;
                    $staffs = $company->sshrFns->loadByCompanyIdActualCountStaff($key);
                    if (!empty($staffs)) {
                        $number_staff = $staffs['number_staff'];
                    }
                    $found['found']['data'][$key]['number_staff'] = $number_staff;
                }
            }
        } else if ($contrType != 'person') {
            $iterationsCount = ceil($arrayCount / 1000);
            for ($i = 1; $i <= $iterationsCount; $i++) {
                $offset = ($i > 1) ? 1000 * ($i - 1) : 0;
                $slice = array_slice($found['found']['data'], $offset, 1000, true);
                $personIds = array_map(function ($el) {
                    return $el['id'];
                }, $slice);
                $allPhones = $person->contacts->loadPhonesByPersonIds($personIds);
                $individualPreporiator = $ip->loadByIds($this->array_value_recursive($slice));
                if (!empty($found['found']['data']) && empty(array_keys($found['found']['data'])[0])) {
                    $found['found']['data'] = array_combine(array_column($found['found']['data'], 'person_id'), $found['found']['data']);
                }
                foreach ($individualPreporiator as $contr) {
                    $found['found']['data'][$contr['person_id']] = $contr;
                    // телефоны
                    $personPhones = [];
                    if (!empty($allPhones)) {
                        foreach ($allPhones as $ph) {
                            if ($ph['person_id'] == $contr['person_id'] && (!empty($ph['number']) || !empty($ph['phone_number']))) {
                                $tmp = !empty($ph['number']) ? $ph['number'] : $ph['phone_number'];
                                if ($ph['type'] == 2) $tmp .= " (факс)";
                                $tmp = trim($tmp);
                                if ($tmp) {
                                    $personPhones[] = $tmp;
                                }
                            }
                        }
                    }
                    $found['found']['data'][$contr['person_id']]['contact'] = (!empty($personPhones)) ? implode(", ", $personPhones) : '';
                }
            }
        }
        # название параметра который хранит историю количества выгрузок
        $reportConfigName = 'report-counts';
        $users = new Users();

        $reportCountsConfig = $users->getConfigParam($params['user_id'], $reportConfigName, true);
        $reportCunts = [];
        if (!empty($reportCountsConfig['parameter_value'])) {
            $reportCunts = json_decode($reportCountsConfig['parameter_value'], true);
        }
        if ($contrType == 'person') {
            $acceptAgreementObj = new AcceptAgreement();
            $found['found']['data'] = $acceptAgreementObj->hideInfoSearchPage($params, $found['found']['data'], true);
            $hidden = $acceptAgreementObj->hiddenFullDataPerson($params, $found['found']['data']);
            $found['found']['data'] = $hidden['data'];
            $found['found']['total_count'] -=  $hidden['count_hidden'];
        }

        # сохранение информации о текущей выгрузке
        $reportCunts[time()] = $found['found']['total_count'];
        $users->setConfigParam($params['user_id'], $reportConfigName, json_encode($reportCunts), true);

        // Формирование и скачивание результатов поиска
        $docReport = new Core();
        if ($formatId == 7) { # в формате docx
         
            $docReport->createSearchReport($found, $allGetValues['contractor']);
        } elseif ($formatId == 2) { # в формате  pdf
            // Формирование docx
            $tmp = time() . rand(0, time());
            $tmpDocFile = sys_get_temp_dir() . '/' . $tmp . '.docx';
            $tmpPdfFile = sys_get_temp_dir() . '/' . $tmp . '.pdf';
            $docObject = $docReport->createSearchReport($found, $allGetValues['contractor'], $tmp);
            if (!$docObject) {
                //$message = ": Не удалось сформировать досье в формате docx по контрагенту с id: " . $contrId . ".";
                //$this->contractorEvents->callTriggerContractorError($this->getEvent(),$message);
                return false;
            }
            // Конвертирование в pdf
            $this->convertToPdf(sys_get_temp_dir(), $tmpDocFile);
            $data = file_get_contents($tmpPdfFile);
            unlink($tmpDocFile);
            unlink($tmpPdfFile);
            // Скачивание pdf
//            echo "sergey <pre>".print_r($contrId,true)."</pre>";exit;//todo: remove
            if ($this->download($data, 2, $contrId, $contrType, "Результат простого поиска") === false) {
                return false;
            }
        } elseif ($formatId == 6) { # в формате xls
            $docReport->createSearchReportExcel($found, $allGetValues['contractor']);
        }
        return true;
    }