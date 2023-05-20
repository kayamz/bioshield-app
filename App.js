import React, { useState, useEffect } from 'react';
import {
	ActivityIndicator,
	Text,
	Image,
	Dimensions,
	Alert,
} from 'react-native';
import styled from 'styled-components';

import { Camera } from 'expo-camera';
import * as ImagePicker from 'expo-image-picker';
import * as MediaLibrary from 'expo-media-library';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as FileSystem from 'expo-file-system';
import * as Sharing from 'expo-sharing';

import { imageTransfer } from './API/api';

import TakePhotoBtn from './Buttons/MainScreenBtns/TakePhotoBtn/TakePhotoPresenter';
import { useTakePhotoState } from './Buttons/MainScreenBtns/TakePhotoBtn/TakePhotoContainer';

import SwitchCameraBtn from './Buttons/MainScreenBtns/SwitchCameraBtn/SwitchCameraPresenter';
import { useCameraTypeState } from './Buttons/MainScreenBtns/SwitchCameraBtn/SwitchCameraContainer';

import GetPhotoBtn from './Buttons/MainScreenBtns/GetPhotoBtn/GetPhotoPresenter';
import { useGetPhotoState } from './Buttons/MainScreenBtns/GetPhotoBtn/GetPhotoContainer';

import TransferBtn from './Buttons/TransferCancelBtns/TransferBtn/TransferPresenter';
import NextBtn from './Buttons/ChangeBtns/NextBtn/NextPresenter';
import CancelBtn from './Buttons/TransferCancelBtns/CancelBtn/CancelPresenter';

import SaveBtn from './Buttons/SaveShareBtns/SaveBtn/SavePresenter';
import ShareBtn from './Buttons/SaveShareBtns/ShareBtn/SharePresenter';

import afterImage from './DetectionServer/testing/img/final/after.png'

const { width, height } = Dimensions.get('window');
const MainContainer = styled.View`
	flex: 1;
	background-color: white;
`;
const MainBtnContainer = styled.View`
	flex: 1;
	width: 100%;
	flex-direction: row;
	justify-content: space-around;
	align-items: center;
`;

// Image Temporary Storage
let firstPhoto = '';
let resultPhotoList = []

export default function App() {
	// useState
	const [hasPermission, setHasPermission] = useState(null);
	const [hasAlbumPermission, setHasAlbumPermission] = useState(false);
	const [isLoading, setIsLoading] = useState(false);
	const [isAfterView, setIsAfterView] = useState(false);

	// Own Hooks States
	const {
		cameraRef,
		isPreview,
		setIsPreview,
		takePhoto,
		setTakePhoto,
		onPressTakePhoto,
	} = useTakePhotoState();
	const {
		imageSelected,
		setImageSelected,
		onPressGetPhoto,
		albumPhoto,
		setAlbumPhoto,
	} = useGetPhotoState();
	const { cameraType, switchCameraType } = useCameraTypeState();
	const {
		isNotice,
		setIsNotice,
	} = useNoticeState();

	// useEffect
	useEffect(() => {
		(async () => {
			// Camera 권한 체크
			const { status } = await Camera.requestCameraPermissionsAsync();
			setHasPermission(status == 'granted');

			// Album 권한 체크
			const {
				status: albumStatus,
			} = await ImagePicker.requestMediaLibraryPermissionsAsync()
			setHasAlbumPermission(albumStatus === 'granted');

			// 안내문 다시보지 않기 체크
			const noticeStatus = await AsyncStorage.getItem('Notice');
			noticeStatus !== null
				? setIsNotice(JSON.parse(noticeStatus))
				: false;
		})();
	}, []);

	const onPressNext = async () => {
		if (isPreview) {
			await cameraRef.current.resumePreview();
			setIsPreview(false);
		}

		if (imageSelected) {
			setImageSelected(false);
		}

		firstPhoto =
			(takePhoto && takePhoto.base64) ||
			(albumPhoto && albumPhoto.base64);

		setTakePhoto({});
		setAlbumPhoto({});
	};

	// 취소 버튼, 모든 상태 초기화
	const onPressCancel = async () => {
		if (isPreview) {
			await cameraRef.current.resumePreview();
			setIsPreview(false);
			setTakePhoto({});
		}

		if (imageSelected) {
			setImageSelected(false);
			setAlbumPhoto({});
		}

		setIsGender('female');
		setGenderValue(false);

		setIsTwoPeople(false);
		setTwoPeopleToggleValue(false);

		setIsAfterView(false);
		firstPhoto = '';
		secondPhoto = '';
		setTakePhoto({});
		setAlbumPhoto({});
	};

		// Server로 이미지 전송하는 버튼
	const getTransferImage = async () => {
		try {
			console.log(`getTransferImage start!`);

			firstPhoto = (takePhoto && takePhoto.base64) || (albumPhoto && albumPhoto.base64);

			// Image Transformation Start

			resultPhotoList = await imageTransfer(firstPhoto);
			resultPhoto = resultPhotoList[1]
			// console.log(resultPhoto.length)
			
			if (isPreview) {
				await cameraRef.current.resumePreview();
				setIsPreview(false);
			}

			if (imageSelected) {
				setImageSelected(false);
			}

			firstPhoto = '';
			setIsAfterView(true);
		} catch (e) {
			alert(`getTransferImage Error: ${e}`);
		}
	};
	

	// 결과 이미지 저장 버튼
	const onPressSave = async () => {
		try {
			resultPhotoList = await imageTransfer(firstPhoto);
			resultPhoto = resultPhotoList[1]

			const changedImg = resultPhotoList[1].split('data:image/png;base64,')[1];
			const changedFileName = FileSystem.documentDirectory + 'changed.png';
			await FileSystem.writeAsStringAsync(changedFileName, changedImg, {
				encoding: FileSystem.EncodingType.Base64,
			});
	  
			// Original, Changed 모두 갤러리 저장
			await MediaLibrary.saveToLibraryAsync(changedFileName);
			Alert.alert('저장완료!', '갤러리에서 확인할 수 있습니다.');
		} catch (error) {
			alert(`Save Result Photo Error: ${error}`);
		}
	};

	// 공유 버튼
	const onPressShare = async () => {
		try {
			// changed Image 공유
			resultPhotoList = await imageTransfer(firstPhoto);
			resultPhoto = resultPhotoList[1]

			const changedImg = resultPhotoList[1].split('data:image/png;base64,')[1];
			const changedFileName = FileSystem.documentDirectory + 'changed.png';
			await FileSystem.writeAsStringAsync(changedFileName, changedImg, {
				encoding: FileSystem.EncodingType.Base64,
      		});
			// changed Image 공유
			await Sharing.shareAsync(changedFileName);
			
		} catch (error) {
			alert(`Open Sharing Error: ${error}`);
		}
	};

	if (hasPermission === true) {
		return (
			<MainContainer>
				{!imageSelected && !isAfterView && (
					<Camera
						style={
							height >= 790
								? {
										alignItems: 'center',
										width: width,
										height: width / 0.75,
										marginTop: 50,
								  }
								: {
										alignItems: 'center',
										width: width,
										height: width / 0.7,
										marginTop: 0,
								  }
						}
						type={cameraType}
						ref={cameraRef}
					>
					</Camera>
				)}

				{imageSelected && (
					<>
						<Image
							style={
								height >= 790
									? {
											width: width,
											height: width / 0.75,
											marginTop: 50,
									  }
									: {
											width: width,
											height: width / 0.75,
											marginTop: 25,
									  }
							}
							source={{ uri: albumPhoto.uri }}
						/>
					</>
				)}

				{isAfterView && (
					<Image
						style={
							height >= 790
								? {
										width: width,
										height: width / 0.75,
										marginTop: 50,
								  }
								: {
										width: width,
										height: width / 0.75,
										marginTop: 25,
								  }
						}
						source={afterImage}
					/>
				)}

				{!isPreview && !imageSelected && !isAfterView && (
					<MainBtnContainer>
						<GetPhotoBtn onPress={onPressGetPhoto} />
						<TakePhotoBtn onPress={onPressTakePhoto} />
						<SwitchCameraBtn onPress={switchCameraType} />
					</MainBtnContainer>
				)}
				{isAfterView && (
					<MainBtnContainer>
						<SaveBtn onPress={onPressSave} />
						<ShareBtn onPress={onPressShare} />
						<CancelBtn onPress={onPressCancel} />
					</MainBtnContainer>
				)}
				{(isPreview || imageSelected) && (
					<MainBtnContainer>
						{!isTwoPeople || (isTwoPeople && firstPhoto) ? (
							<TransferBtn onPress={getTransferImage} />
						) : (
							<NextBtn onPress={onPressNext} />
						)}
						<CancelBtn onPress={onPressCancel} />
					</MainBtnContainer>
				)}
			</MainContainer>
		);
	} else if (hasPermission === false) {
		return (
			<MainContainer>
				<Text>Don't have permission for this</Text>
			</MainContainer>
		);
	} else {
		return (
			<MainContainer>
				<ActivityIndicator />
			</MainContainer>
		);
	}
}