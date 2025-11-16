/**
 * Fashion Try-On Frontend Application
 * Handles image upload, API calls, and result display
 */

// Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    POLL_INTERVAL: 3000, // 3 seconds
    MAX_POLL_ATTEMPTS: 100,
};

// State
const state = {
    modelImage: null,
    garmentImage: null,
    currentTaskId: null,
    pollInterval: null,
};

// DOM Elements
const elements = {
    modelImage: document.getElementById('modelImage'),
    garmentImage: document.getElementById('garmentImage'),
    modelUploadArea: document.getElementById('modelUploadArea'),
    garmentUploadArea: document.getElementById('garmentUploadArea'),
    modelPreview: document.getElementById('modelPreview'),
    garmentPreview: document.getElementById('garmentPreview'),
    tryOnBtn: document.getElementById('tryOnBtn'),
    progressSection: document.getElementById('progressSection'),
    resultSection: document.getElementById('resultSection'),
    statusText: document.getElementById('statusText'),
    taskId: document.getElementById('taskId'),
    progressFill: document.getElementById('progressFill'),
    progressPercentage: document.getElementById('progressPercentage'),
    progressDetails: document.getElementById('progressDetails'),
    resultOriginal: document.getElementById('resultOriginal'),
    resultGarment: document.getElementById('resultGarment'),
    resultImage: document.getElementById('resultImage'),
    processingTime: document.getElementById('processingTime'),
    usedProvider: document.getElementById('usedProvider'),
    downloadBtn: document.getElementById('downloadBtn'),
    newTryBtn: document.getElementById('newTryBtn'),
    denoiseSteps: document.getElementById('denoiseSteps'),
    denoiseValue: document.getElementById('denoiseValue'),
    toast: document.getElementById('toast'),
};

// ============= Utility Functions =============

function showToast(message, type = 'info') {
    elements.toast.textContent = message;
    elements.toast.className = `toast show ${type}`;
    setTimeout(() => {
        elements.toast.classList.remove('show');
    }, 3000);
}

function updateProgress(percentage, status) {
    elements.progressFill.style.width = `${percentage}%`;
    elements.progressPercentage.textContent = `${percentage}%`;
    elements.statusText.textContent = status;
}

// ============= Image Upload Handling =============

function setupImageUpload(inputElement, uploadArea, previewElement, stateKey) {
    // File input change
    inputElement.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleImageFile(file, previewElement, stateKey);
        }
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');

        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleImageFile(file, previewElement, stateKey);
        } else {
            showToast('Vui lòng chọn file ảnh hợp lệ', 'error');
        }
    });
}

function handleImageFile(file, previewElement, stateKey) {
    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        showToast('File quá lớn! Tối đa 10MB', 'error');
        return;
    }

    // Validate file type
    if (!file.type.startsWith('image/')) {
        showToast('File không phải ảnh!', 'error');
        return;
    }

    // Store file
    state[stateKey] = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewElement.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
        previewElement.classList.add('active');
    };
    reader.readAsDataURL(file);

    // Enable try-on button if both images are uploaded
    checkEnableTryOn();
}

function checkEnableTryOn() {
    if (state.modelImage && state.garmentImage) {
        elements.tryOnBtn.disabled = false;
    }
}

// ============= API Functions =============

async function createTryOnTask() {
    const formData = new FormData();
    formData.append('model_image', state.modelImage);
    formData.append('garment_image', state.garmentImage);

    // Get selected provider
    const provider = document.querySelector('input[name="provider"]:checked').value;
    formData.append('provider', provider);

    // Get category
    const category = document.getElementById('category').value;
    formData.append('category', category);

    // Get denoise steps
    const denoiseSteps = elements.denoiseSteps.value;
    formData.append('denoise_steps', denoiseSteps);

    // Get seed
    const seed = document.getElementById('seed').value;
    formData.append('seed', seed);

    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/v1/tryon`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Lỗi khi tạo task');
        }

        return await response.json();
    } catch (error) {
        console.error('Error creating task:', error);
        throw error;
    }
}

async function getTaskStatus(taskId) {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/v1/tryon/${taskId}`);

        if (!response.ok) {
            throw new Error('Lỗi khi kiểm tra trạng thái');
        }

        return await response.json();
    } catch (error) {
        console.error('Error getting task status:', error);
        throw error;
    }
}

// ============= Task Flow =============

async function startTryOn() {
    try {
        // Disable button and show loading
        elements.tryOnBtn.disabled = true;
        elements.tryOnBtn.innerHTML = '<div class="spinner"></div> <span>Đang khởi tạo...</span>';

        // Hide result section
        elements.resultSection.style.display = 'none';

        // Show progress section
        elements.progressSection.style.display = 'block';
        updateProgress(0, 'Đang tải ảnh lên server...');

        // Create task
        const taskData = await createTryOnTask();
        state.currentTaskId = taskData.task_id;

        elements.taskId.textContent = taskData.task_id;
        showToast('Task đã được tạo thành công!', 'success');

        // Start polling
        updateProgress(10, 'Task đã được tạo, đang chờ xử lý...');
        elements.progressDetails.textContent = `Provider: ${document.querySelector('input[name="provider"]:checked').value} | ${taskData.message}`;

        pollTaskStatus();

    } catch (error) {
        showToast(error.message || 'Có lỗi xảy ra!', 'error');
        elements.tryOnBtn.disabled = false;
        elements.tryOnBtn.innerHTML = '<span class="btn-icon">✨</span><span class="btn-text">Bắt Đầu Thử Đồ</span>';
        elements.progressSection.style.display = 'none';
    }
}

function pollTaskStatus() {
    let attempts = 0;

    state.pollInterval = setInterval(async () => {
        attempts++;

        if (attempts > CONFIG.MAX_POLL_ATTEMPTS) {
            clearInterval(state.pollInterval);
            showToast('Task timeout - Quá thời gian chờ!', 'error');
            resetUI();
            return;
        }

        try {
            const status = await getTaskStatus(state.currentTaskId);

            updateProgress(status.progress, `Trạng thái: ${status.status}`);

            if (status.status === 'completed') {
                clearInterval(state.pollInterval);
                showResult(status);
            } else if (status.status === 'failed') {
                clearInterval(state.pollInterval);
                showToast(`Task thất bại: ${status.error_message}`, 'error');
                resetUI();
            } else if (status.status === 'processing') {
                elements.progressDetails.textContent = '🔄 Đang xử lý ảnh với AI model... Vui lòng đợi (20-60 giây)';
            }

        } catch (error) {
            console.error('Poll error:', error);
        }
    }, CONFIG.POLL_INTERVAL);
}

function showResult(status) {
    // Hide progress
    elements.progressSection.style.display = 'none';

    // Show result
    elements.resultSection.style.display = 'block';

    // Set images
    const resultUrl = `${CONFIG.API_BASE_URL}${status.result_url}`;

    // Show original images
    const modelReader = new FileReader();
    modelReader.onload = (e) => {
        elements.resultOriginal.src = e.target.result;
    };
    modelReader.readAsDataURL(state.modelImage);

    const garmentReader = new FileReader();
    garmentReader.onload = (e) => {
        elements.resultGarment.src = e.target.result;
    };
    garmentReader.readAsDataURL(state.garmentImage);

    // Show result image
    elements.resultImage.src = resultUrl;
    elements.resultImage.onload = () => {
        showToast('🎉 Hoàn thành! Kết quả đã sẵn sàng', 'success');
    };

    // Set stats
    elements.processingTime.textContent = status.processing_time
        ? `${status.processing_time.toFixed(2)}s`
        : 'N/A';
    elements.usedProvider.textContent = document.querySelector('input[name="provider"]:checked').value;

    // Setup download button
    elements.downloadBtn.onclick = () => {
        const link = document.createElement('a');
        link.href = resultUrl;
        link.download = `fashion-tryon-${state.currentTaskId}.jpg`;
        link.click();
    };

    // Reset UI
    resetUI();

    // Scroll to result
    elements.resultSection.scrollIntoView({ behavior: 'smooth' });
}

function resetUI() {
    elements.tryOnBtn.disabled = false;
    elements.tryOnBtn.innerHTML = '<span class="btn-icon">✨</span><span class="btn-text">Bắt Đầu Thử Đồ</span>';
}

function resetAll() {
    // Reset state
    state.modelImage = null;
    state.garmentImage = null;
    state.currentTaskId = null;

    // Clear previews
    elements.modelPreview.innerHTML = '';
    elements.modelPreview.classList.remove('active');
    elements.garmentPreview.innerHTML = '';
    elements.garmentPreview.classList.remove('active');

    // Clear inputs
    elements.modelImage.value = '';
    elements.garmentImage.value = '';

    // Hide sections
    elements.progressSection.style.display = 'none';
    elements.resultSection.style.display = 'none';

    // Disable button
    elements.tryOnBtn.disabled = true;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============= Event Listeners =============

function initializeApp() {
    // Setup image uploads
    setupImageUpload(
        elements.modelImage,
        elements.modelUploadArea,
        elements.modelPreview,
        'modelImage'
    );

    setupImageUpload(
        elements.garmentImage,
        elements.garmentUploadArea,
        elements.garmentPreview,
        'garmentImage'
    );

    // Try-on button
    elements.tryOnBtn.addEventListener('click', startTryOn);

    // New try button
    elements.newTryBtn.addEventListener('click', resetAll);

    // Denoise steps slider
    elements.denoiseSteps.addEventListener('input', (e) => {
        elements.denoiseValue.textContent = e.target.value;
    });

    // Provider selection animation
    document.querySelectorAll('.provider-card').forEach(card => {
        card.addEventListener('click', () => {
            document.querySelectorAll('.provider-card').forEach(c => {
                c.classList.remove('selected');
            });
            card.classList.add('selected');
        });
    });

    // Check API health on load
    checkAPIHealth();
}

async function checkAPIHealth() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/`);
        if (response.ok) {
            const data = await response.json();
            console.log('API Health:', data);

            // Show warning if providers not available
            if (!data.on_premise_available && !data.external_api_available) {
                showToast('⚠️ Chưa có provider nào được cấu hình! Kiểm tra .env file', 'warning');
            }
        }
    } catch (error) {
        showToast('⚠️ Không thể kết nối đến API server. Vui lòng chạy backend!', 'error');
        console.error('API Health Check Failed:', error);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

// Prevent form submission
document.addEventListener('submit', (e) => {
    e.preventDefault();
});

console.log('🚀 Fashion Try-On App initialized!');
console.log('📍 API URL:', CONFIG.API_BASE_URL);
