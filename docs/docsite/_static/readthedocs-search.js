document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.querySelector('.st-default-search-input');
  if (!searchInput) {
    return;
  }
  const showSearch = () => {
    document.dispatchEvent(new CustomEvent('readthedocs-search-show'));
  };
  searchInput.addEventListener('focusin', showSearch);
  searchInput.addEventListener('click', showSearch);
});
