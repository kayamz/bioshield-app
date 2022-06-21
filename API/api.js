import axios from 'axios';
import { Alert } from 'react-native';
import { SERVER_IP, SERVER_PORT } from './apiAddress.js';

const URL = `http://${SERVER_IP}:${SERVER_PORT}/let_me_shine`;

let tempResult = [];

const getResults = (imgObj) => {
	console.log('[3] Image Transfer Start!');
	const after = `${imgObj.after}`;
	const after64 = `data:image/png;base64,${imgObj.after64}`;
	// console.log(after);
	// console.log(after64);
	console.log('[3] Image Transfer Complete!');
	tempResult = [after, after64];
};

const getResultURL = async (url) => {
	try {
		console.log('[2] Get Start!');

		await axios
			.get(url) // get으로 해당 url에 접근
			.then((res) => getResults(res.data.results))
			// getResults 함수로 보낸다.
			.catch((err) => console.log(`Get axios error: ${err}`));

		console.log('[2] Get End!');
	} catch (e) {
		console.log(`getResultURL Error: ${e}`);
	}
};

export const imageTransfer = async (firstPhoto) => {
	try {
		console.log('[1] Post Start!');
		const config = {
			// 보내는 파일의 타입 설정
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*',
			},
		};
		await axios
			.post(
				URL,
				{
					label: 'Image',
					origin: firstPhoto
				},
				config
                ) // 해당 URL로 POST
			.then((res) => getResultURL(res.data))
			// POST의 결과(res)로부터 모델 결과 위치(res.data) 얻음
			// 이를 getResultURL 함수로 보낸다.
			.catch((err) => {
				console.log(`Post axios error: ${err}`);
				error = false;
				Alert.alert(
					'사람을 찍어주세요🤣',
					'만약 사람이라면 눈을 조금만 더 크게 떠주세요😘'
				);
			});
		console.log('[1] Post End!');
	} catch (e) {
		console.log(`imageTransfer Error: ${e}`);
        Alert.alert(
            'imageTransfer Error🤣',
        );
        }finally {
            const result = tempResult;
			if (result.length === 2) {
				return result;
			} else {
				return false;
			}
        }
};