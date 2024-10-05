const loadMoreButton = document.getElementById('loadMore');

loadMoreButton.addEventListener('click', () => {
    const newArticle = document.createElement('article');
    newArticle.classList.add('tease-card');
    newArticle.innerHTML = `
        <h2>Headline 4: New Discoveries!</h2>
        <p>Scientists are making new discoveries every day.</p>
    `;
    document.querySelector('.news-container').appendChild(newArticle);
});
