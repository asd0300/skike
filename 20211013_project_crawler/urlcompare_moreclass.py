{"operationName":"intlFlightListSearch","variables":{"request":{"Head":{"Currency":"TWD","ExtendFields":{"SpecialSupply":"false"}},"mode":1,"searchNo":1,"criteriaToken":"","productKeyInfo":null,"searchInfo":{"tripType":"OW","cabinClass":"YS","searchSegmentList":[{"dCityCode":"TPE","aCityCode":"SEL","dDate":"2021-11-26"}],"travelerNum":{"adult":1,"child":0,"infant":0},"openRtMergeSearch":false}}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"147190e96069b1cc2e3c2b03044c3ed25da27a44d9931d4ab2a3293abc875788"}}}
#1
{"operationName":"intlFlightMoreGradeSearch","variables":{"request":{"Head":{"Currency":"TWD"},"criteriaToken":"tripType:OW|criteriatoken:KLUv_QBQKQIACwgBEJSoARjTggMggNiqzNUvDBMIARABGAEUGAMgASgLMBlDKAAwADgAQABIAFAAgAEAkAEAqAEAuAEAREgAUABg1IsB|cabinClass:YSGroup|adult:1|dCity_1:TPE|aCity_1:SEL|date_1:2021-11-26|idc:SHAXY|extensionflag:0","lowPrice":10381,"origDestRequestInfoList":[{"segmentNo":1,"flightNo":"KE692","departureDate":"2021-11-26","airlineCode":"KE"}]}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"286bf26e592e818dba393cfef4cc9108ccdf23c0b832516620cb0bba6b81abd2"}}}
#2
{"operationName":"intlFlightMoreGradeSearch","variables":{"request":{"Head":{"Currency":"TWD"},"criteriaToken":"tripType:OW|criteriatoken:KLUv_QBQKQIACwgBEJSoARjTggMggNiqzNUvDBMIARABGAEUGAMgASgLMBlDKAAwADgAQABIAFAAgAEAkAEAqAEAuAEAREgAUABg1IsB|cabinClass:YSGroup|adult:1|dCity_1:TPE|aCity_1:SEL|date_1:2021-11-26|idc:SHAXY|extensionflag:0","lowPrice":10358,"origDestRequestInfoList":[{"segmentNo":1,"flightNo":"BR160","departureDate":"2021-11-26","airlineCode":"BR"}]}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"286bf26e592e818dba393cfef4cc9108ccdf23c0b832516620cb0bba6b81abd2"}}}

#3
{"operationName":"intlFlightMoreGradeSearch","variables":{"request":{"Head":{"Currency":"TWD"},"criteriaToken":"tripType:OW|criteriatoken:KLUv_QBQKQIACwgBEJSoARjTggMggNiqzNUvDBMIARABGAEUGAMgASgLMBlDKAAwADgAQABIAFAAgAEAkAEAqAEAuAEAREgAUABg1IsB|cabinClass:YSGroup|adult:1|dCity_1:TPE|aCity_1:SEL|date_1:2021-11-26|idc:SHAXY|extensionflag:0","lowPrice":10923,"origDestRequestInfoList":[{"segmentNo":1,"flightNo":"OZ6872","departureDate":"2021-11-26","airlineCode":"OZ"}]}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"286bf26e592e818dba393cfef4cc9108ccdf23c0b832516620cb0bba6b81abd2"}}}

{
    "data": {
        "intlFlightMoreGradeSearch": {
            "ResponseStatus": {
                "Ack": "Success",
                "__typename": "ResponseStatusPayload"
            },
            "responseHead": {
                "errorCode": "0",
                "errorMessage": "",
                "__typename": "ResponseHeadPayload"
            },
            "productInfo": {
                "policyInfoList": [
                    {
                        "remarkTokenKey": "d28d941a1627aaa3fa34f0dea84412d9",
                        "productFlag": 0,
                        "channelInfoList": [
                            {
                                "engineType": "Ctrip",
                                "channelType": "GDS-WS",
                                "__typename": "ChannelInfoPayload"
                            }
                        ],
                        "productClass": [
                            "經濟艙"
                        ],
                        "mainClass": "Economy",
                        "availableTickets": 9,
                        "priceDetailInfo": {
                            "originalViewAvgPrice": null,
                            "viewAvgPrice": 10526,
                            "viewTotalPrice": 10526,
                            "adult": {
                                "totalPrice": 10526,
                                "tax": 1615,
                                "fare": 8911,
                                "discount": null,
                                "extraFee": null,
                                "bookingFee": 0,
                                "atolFee": null,
                                "__typename": "TravelerPricePayload"
                            },
                            "child": null,
                            "infant": null,
                            "__typename": "PriceDetailInfoPayload"
                        },
                        "productKeyInfo": {
                            "groupKey": "BR160-TPE-SEL-20211126^2^KLUv_QBQQQMACwgBEJSoARjTggMggNiqzNUvDBMIARABGAEUGAMgASgLMBlDKAAwADgAQABIAFAAgAEAkAEAqAEAuAEAREgAUABbCwgBEAAaACAAKIIJMKABOABAAEiA2KrM1S9QAFgADBAGXGDUiwE=^^True^10526.0^Ctrip|NA|NA|0|8911.0,1615.0,YNLH-BR|ADT^BR160|1|2021-11-26 00:00:00^zh_hk",
                            "shoppingId": "8000000108H5W07w00e4WX800000000020000000000100sOt510G004o8YwW02Tjm800DnhKWY33",
                            "__typename": "ProductKeyInfoPayload"
                        },
                        "flightPromptInfoList": null,
                        "travelerEligibilityList": [
                            "ADT"
                        ],
                        "limitInfo": {
                            "nationalityLimitType": 0,
                            "nationalityLimit": [],
                            "minAge": 0,
                            "maxAge": 99,
                            "minPassengerCount": 1,
                            "maxPassengerCount": 9,
                            "localDocumentsLimitList": [],
                            "__typename": "LimitInfoPayload"
                        },
                        "ticketDeadlineInfo": {
                            "deadlineType": 1,
                            "promiseMinutes": 1440,
                            "__typename": "TicketDeadlineInfoPayload"
                        },
                        "whetherNonCard": null,
                        "agencyTag": "GDS-WS|YNLH",
                        "recommend": null,
                        "limitTimeFreeInfo": null,
                        "hasFreeCoupon": false,
                        "descriptionInfo": {
                            "productName": "延遲出票",
                            "productCategory": "Exclusive",
                            "ticketDescription": "付款成功後，將於24小時內出票。",
                            "__typename": "DescriptionInfoPayload"
                        },
                        "multiTicketInfo": null,
                        "couponInfoList": null,
                        "hasMemberPrice": false,
                        "promoFundInfo": null,
                        "kRCreditCardPromotionList": null,
                        "baggageIncluded": 1,
                        "canFlexibleChange": false,
                        "hasAgencyModel": false,
                        "hasBrandTier": false,
                        "isMoreGradeResult": true,
                        "creditCardPaymentInfoRefNumList": [],
                        "hasAtol": false,
                        "brandTier": -1,
                        "policyTags": null,
                        "__typename": "PolicyInfoPayload"
                    },
                    {
                        "remarkTokenKey": "3371534943beb3d6f356da2eeee933a9",
                        "productFlag": 0,
                        "channelInfoList": [
                            {
                                "engineType": "Ctrip",
                                "channelType": "GDS-WS",
                                "__typename": "ChannelInfoPayload"
                            }
                        ],
                        "productClass": [
                            "經濟艙"
                        ],
                        "mainClass": "Economy",
                        "availableTickets": 9,
                        "priceDetailInfo": {
                            "originalViewAvgPrice": null,
                            "viewAvgPrice": 10558,
                            "viewTotalPrice": 10558,
                            "adult": {
                                "totalPrice": 10558,
                                "tax": 1615,
                                "fare": 8943,
                                "discount": null,
                                "extraFee": null,
                                "bookingFee": 0,
                                "atolFee": null,
                                "__typename": "TravelerPricePayload"
                            },
                            "child": null,
                            "infant": null,
                            "__typename": "PriceDetailInfoPayload"
                        },
                        "productKeyInfo": {
                            "groupKey": "BR160-TPE-SEL-20211126^2^KLUv_QBQQQMACwgBEJSoARjTggMggNiqzNUvDBMIARABGAEUGAMgASgLMBlDKAAwADgAQABIAFAAgAEAkAEAqAEAuAEAREgAUABbCwgBEAAaACAAKIIJMKABOABAAEiA2KrM1S9QAFgADBAGXGDUiwE=^^True^10558.0^Ctrip|NA|NA|0|8943.0,1615.0,USRH-BR|ADT^BR160|1|2021-11-26 00:00:00^zh_hk",
                            "shoppingId": "8000000108H5W07w00e4WX800000000020000000000100sbN510G006g8YwW02Tjm8002AJ4WY4a",
                            "__typename": "ProductKeyInfoPayload"
                        },
                        "flightPromptInfoList": null,
                        "travelerEligibilityList": [
                            "ADT"
                        ],
                        "limitInfo": {
                            "nationalityLimitType": 0,
                            "nationalityLimit": [],
                            "minAge": 0,
                            "maxAge": 99,
                            "minPassengerCount": 1,
                            "maxPassengerCount": 9,
                            "localDocumentsLimitList": [],
                            "__typename": "LimitInfoPayload"
                        },
                        "ticketDeadlineInfo": {
                            "deadlineType": 1,
                            "promiseMinutes": 120,
                            "__typename": "TicketDeadlineInfoPayload"
                        },
                        "whetherNonCard": null,
                        "agencyTag": "GDS-WS|USRH",
                        "recommend": null,
                        "limitTimeFreeInfo": null,
                        "hasFreeCoupon": false,
                        "descriptionInfo": {
                            "productName": "推薦",
                            "productCategory": "Prioritizing",
                            "ticketDescription": "付款成功後，將於2小時內出票。",
                            "__typename": "DescriptionInfoPayload"
                        },
                        "multiTicketInfo": null,
                        "couponInfoList": null,
                        "hasMemberPrice": false,
                        "promoFundInfo": null,
                        "kRCreditCardPromotionList": null,
                        "baggageIncluded": 1,
                        "canFlexibleChange": false,
                        "hasAgencyModel": false,
                        "hasBrandTier": false,
                        "isMoreGradeResult": true,
                        "creditCardPaymentInfoRefNumList": [],
                        "hasAtol": false,
                        "brandTier": -1,
                        "policyTags": null,
                        "__typename": "PolicyInfoPayload"
                    },
                    {
                        "remarkTokenKey": "69ec9ccafbd31e30527d6d8ec90b082a",
                        "productFlag": 0,
                        "channelInfoList": [
                            {
                                "engineType": "Pricing",
                                "channelType": "PRC-WS",
                                "__typename": "ChannelInfoPayload"
                            }
                        ],
                        "productClass": [
                            "經濟艙"
                        ],
                        "mainClass": "Economy",
                        "availableTickets": 9,
                        "priceDetailInfo": {
                            "originalViewAvgPrice": null,
                            "viewAvgPrice": 10561,
                            "viewTotalPrice": 10561,
                            "adult": {
                                "totalPrice": 10561,
                                "tax": 1614,
                                "fare": 8947,
                                "discount": null,
                                "extraFee": null,
                                "bookingFee": 0,
                                "atolFee": null,
                                "__typename": "TravelerPricePayload"
                            },
                            "child": null,
                            "infant": null,
                            "__typename": "PriceDetailInfoPayload"
                        },
                        "productKeyInfo": {
                            "groupKey": "BR160-TPE-SEL-20211126^2^KLUv_QBQQQMACwgBEJSoARjTggMggNiqzNUvDBMIARABGAEUGAMgASgLMBlDKAAwADgAQABIAFAAgAEAkAEAqAEAuAEAREgAUABbCwgBEAAaACAAKIIJMKABOABAAEiA2KrM1S9QAFgADBAGXGDUiwE=^^True^10561.0^Pricing|NA|NA|0|8947.0,1614.0,TPYY-BR|ADT^BR160|1|2021-11-26 00:00:00^zh_hk",
                            "shoppingId": "8000000108H5W07w00e4WX800000000020000000000G00scx510G000e8YwW02TdW800yAK4WcMK",
                            "__typename": "ProductKeyInfoPayload"
                        },
                        "flightPromptInfoList": null,
                        "travelerEligibilityList": [
                            "ADT"
                        ],
                        "limitInfo": {
                            "nationalityLimitType": 0,
                            "nationalityLimit": [],
                            "minAge": 0,
                            "maxAge": 99,
                            "minPassengerCount": 1,
                            "maxPassengerCount": 9,
                            "localDocumentsLimitList": [],
                            "__typename": "LimitInfoPayload"
                        },
                        "ticketDeadlineInfo": {
                            "deadlineType": 1,
                            "promiseMinutes": 120,
                            "__typename": "TicketDeadlineInfoPayload"
                        },
                        "whetherNonCard": null,
                        "agencyTag": "PRC-WS|TPYY",
                        "recommend": null,
                        "limitTimeFreeInfo": null,
                        "hasFreeCoupon": false,
                        "descriptionInfo": {
                            "productName": "推薦",
                            "productCategory": "Prioritizing",
                            "ticketDescription": "付款成功後，將於2小時內出票。",
                            "__typename": "DescriptionInfoPayload"
                        },
                        "multiTicketInfo": null,
                        "couponInfoList": null,
                        "hasMemberPrice": false,
                        "promoFundInfo": null,
                        "kRCreditCardPromotionList": null,
                        "baggageIncluded": 1,
                        "canFlexibleChange": false,
                        "hasAgencyModel": false,
                        "hasBrandTier": false,
                        "isMoreGradeResult": true,
                        "creditCardPaymentInfoRefNumList": [],
                        "hasAtol": false,
                        "brandTier": -1,
                        "policyTags": null,
                        "__typename": "PolicyInfoPayload"
                    },
                    {
                        "remarkTokenKey": "ca7af9fc21667cc952a87d034e7156e0",
                        "productFlag": 1024,
                        "channelInfoList": [
                            {
                                "engineType": "Ctrip",
                                "channelType": "GDS-WS",
                                "__typename": "ChannelInfoPayload"
                            }
                        ],
                        "productClass": [
                            "經濟艙"
                        ],
                        "mainClass": "Economy",
                        "availableTickets": 9,
                        "priceDetailInfo": {
                            "originalViewAvgPrice": null,
                            "viewAvgPrice": 22624,
                            "viewTotalPrice": 22624,
                            "adult": {
                                "totalPrice": 22624,
                                "tax": 1615,
                                "fare": 21009,
                                "discount": null,
                                "extraFee": null,
                                "bookingFee": 0,
                                "atolFee": null,
                                "__typename": "TravelerPricePayload"
                            },
                            "child": null,
                            "infant": null,
                            "__typename": "PriceDetailInfoPayload"
                        },
                        "productKeyInfo": {
                            "groupKey": "BR160-TPE-SEL-20211126^2^KLUv_QBQQQMACwgBEJSoARjTggMggNiqzNUvDBMIARABGAEUGAMgASgLMBlDKAAwADgAQABIAFAAgAEAkAEAqAEAuAEAREgAUABbCwgBEAAaACAAKIIJMKABOABAAEiA2KrM1S9QAFgADBAGXGDUiwE=^^True^22624.0^Ctrip|NA|NA|0|21009.0,1615.0,GYDS-BR|ADT^BR160|1|2021-11-26 00:00:00^zh_hk",
                            "shoppingId": "8000000108H6G07w00e4WX8000000000200000000001020Ef510G002E8YwW02Tjm800TbaqWan6",
                            "__typename": "ProductKeyInfoPayload"
                        },
                        "flightPromptInfoList": null,
                        "travelerEligibilityList": [
                            "ADT"
                        ],
                        "limitInfo": {
                            "nationalityLimitType": 0,
                            "nationalityLimit": [],
                            "minAge": 0,
                            "maxAge": 99,
                            "minPassengerCount": 1,
                            "maxPassengerCount": 9,
                            "localDocumentsLimitList": [],
                            "__typename": "LimitInfoPayload"
                        },
                        "ticketDeadlineInfo": {
                            "deadlineType": 1,
                            "promiseMinutes": 120,
                            "__typename": "TicketDeadlineInfoPayload"
                        },
                        "whetherNonCard": null,
                        "agencyTag": "GDS-WS|GYDS",
                        "recommend": null,
                        "limitTimeFreeInfo": null,
                        "hasFreeCoupon": false,
                        "descriptionInfo": {
                            "productName": "推薦",
                            "productCategory": "Prioritizing",
                            "ticketDescription": "付款成功後，將於2小時內出票。",
                            "__typename": "DescriptionInfoPayload"
                        },
                        "multiTicketInfo": null,
                        "couponInfoList": null,
                        "hasMemberPrice": false,
                        "promoFundInfo": null,
                        "kRCreditCardPromotionList": null,
                        "baggageIncluded": 1,
                        "canFlexibleChange": false,
                        "hasAgencyModel": false,
                        "hasBrandTier": false,
                        "isMoreGradeResult": true,
                        "creditCardPaymentInfoRefNumList": [],
                        "hasAtol": false,
                        "brandTier": -1,
                        "policyTags": null,
                        "__typename": "PolicyInfoPayload"
                    },
                    {
                        "remarkTokenKey": "106ce65be80276fbc0fd42b2ca913017",
                        "productFlag": 0,
                        "channelInfoList": [
                            {
                                "engineType": "Ctrip",
                                "channelType": "GDS-WS",
                                "__typename": "ChannelInfoPayload"
                            }
                        ],
                        "productClass": [
                            "商務艙"
                        ],
                        "mainClass": "Business",
                        "availableTickets": 9,
                        "priceDetailInfo": {
                            "originalViewAvgPrice": null,
                            "viewAvgPrice": 25247,
                            "viewTotalPrice": 25247,
                            "adult": {
                                "totalPrice": 25247,
                                "tax": 1614,
                                "fare": 23633,
                                "discount": null,
                                "extraFee": null,
                                "bookingFee": 0,
                                "atolFee": null,
                                "__typename": "TravelerPricePayload"
                            },
                            "child": null,
                            "infant": null,
                            "__typename": "PriceDetailInfoPayload"
                        },
                        "productKeyInfo": {
                            "groupKey": "BR160-TPE-SEL-20211126^2^KLUv_QBQQQMACwgBEJSoARjTggMggNiqzNUvDBMIARABGAEUGAMgASgLMBlDKAAwADgAQABIAFAAgAEAkAEAqAEAuAEAREgAUABbCwgBEAAaACAAKIIJMKABOABAAEiA2KrM1S9QAFgADBAGXGDUiwE=^^True^25247.0^Ctrip|NA|NA|0|23633.0,1614.0,TPYY-BR|ADT^BR160|1|2021-11-26 00:00:00^zh_hk",
                            "shoppingId": "8000000108H1007w00e4WX800000000080000000000102GFf510G000e8YwW02TdW802Au_4WcMK",
                            "__typename": "ProductKeyInfoPayload"
                        },
                        "flightPromptInfoList": null,
                        "travelerEligibilityList": [
                            "ADT"
                        ],
                        "limitInfo": {
                            "nationalityLimitType": 0,
                            "nationalityLimit": [],
                            "minAge": 0,
                            "maxAge": 99,
                            "minPassengerCount": 1,
                            "maxPassengerCount": 9,
                            "localDocumentsLimitList": [],
                            "__typename": "LimitInfoPayload"
                        },
                        "ticketDeadlineInfo": {
                            "deadlineType": 1,
                            "promiseMinutes": 120,
                            "__typename": "TicketDeadlineInfoPayload"
                        },
                        "whetherNonCard": null,
                        "agencyTag": "GDS-WS|TPYY",
                        "recommend": null,
                        "limitTimeFreeInfo": null,
                        "hasFreeCoupon": false,
                        "descriptionInfo": {
                            "productName": "推薦",
                            "productCategory": "Prioritizing",
                            "ticketDescription": "付款成功後，將於2小時內出票。",
                            "__typename": "DescriptionInfoPayload"
                        },
                        "multiTicketInfo": null,
                        "couponInfoList": null,
                        "hasMemberPrice": false,
                        "promoFundInfo": null,
                        "kRCreditCardPromotionList": null,
                        "baggageIncluded": 1,
                        "canFlexibleChange": false,
                        "hasAgencyModel": false,
                        "hasBrandTier": false,
                        "isMoreGradeResult": true,
                        "creditCardPaymentInfoRefNumList": [],
                        "hasAtol": false,
                        "brandTier": -1,
                        "policyTags": null,
                        "__typename": "PolicyInfoPayload"
                    }
                ],
                "__typename": "MoreGradeProductInfoPayload"
            },
            "creditCardPaymentInfoList": null,
            "__typename": "IntlFlightMoreGradeSearchPayload"
        }
    }
}



