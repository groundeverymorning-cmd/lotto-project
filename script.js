document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const ballsContainer = document.querySelector('.balls-container');

    generateBtn.addEventListener('click', () => {
        // 버튼 비활성화 (애니메이션 진행 중 중복 클릭 방지)
        generateBtn.disabled = true;
        generateBtn.style.opacity = '0.7';
        generateBtn.style.cursor = 'not-allowed';

        // 기존 요소 초기화
        ballsContainer.innerHTML = '';

        // 1부터 45까지 중복 없는 숫자 6개 생성
        const numbers = new Set();
        while(numbers.size < 6) {
            numbers.add(Math.floor(Math.random() * 45) + 1);
        }

        // 숫자 오름차순 정렬
        const sortedNumbers = Array.from(numbers).sort((a, b) => a - b);

        // 공 생성 및 애니메이션 적용
        sortedNumbers.forEach((num, index) => {
            const ball = document.createElement('div');
            ball.className = `ball ${getColorClass(num)}`;
            ball.textContent = num;
            
            ballsContainer.appendChild(ball);

            // 순차적 애니메이션 (0.3초 간격)
            setTimeout(() => {
                ball.classList.add('show');
                ball.classList.add('pop');
            }, 300 * index);
        });

        // 애니메이션 완료 후 버튼 원상복구
        setTimeout(() => {
            generateBtn.disabled = false;
            generateBtn.style.opacity = '1';
            generateBtn.style.cursor = 'pointer';
        }, 300 * 6);
    });

    // 숫자 대역에 따른 색상 클래스 반환
    function getColorClass(number) {
        if (number <= 10) return 'color-1'; // 1~10
        if (number <= 20) return 'color-2'; // 11~20
        if (number <= 30) return 'color-3'; // 21~30
        if (number <= 40) return 'color-4'; // 31~40
        return 'color-5'; // 41~45
    }
});
