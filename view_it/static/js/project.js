import '../sass/project.scss';
import 'keen-slider/keen-slider.min.css';
import { MeiliSearch } from 'meilisearch';

addEventListener('DOMContentLoaded', async (event) => {
  const client = new MeiliSearch({
    host: 'http://localhost:7700',
  });

  const index = await client.index('videos');

  document
    .getElementById('meili')
    .addEventListener('keyup', async function (event) {
      populateResults(await searchIndex(index, this.value));
    });
});

async function searchIndex(index, input) {
  return await index.search(input);
}

async function populateResults(results) {
  const dropdown = document.getElementById('meili-results');
  dropdown.innerHTML = '';
  for (let i in results.hits) {
    let li = document.createElement('li');
    let a = document.createElement('a');

    a.classList.add('dropdown-item');
    a.href = results.hits[i].url;
    a.textContent = results.hits[i].title;

    li.appendChild(a);
    dropdown.appendChild(li);
  }
}
