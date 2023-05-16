import '../sass/project.scss';
import { MeiliSearch } from 'meilisearch';
import { instantMeiliSearch } from '@meilisearch/instant-meilisearch';
import instantsearch from 'instantsearch.js';
import { searchBox } from 'instantsearch.js/es/widgets';
import { connectAutocomplete } from 'instantsearch.js/es/connectors';

addEventListener('DOMContentLoaded', async (event) => {
  let index = await indexExists();

  if (index) {
    const searchClient = new instantMeiliSearch('http://localhost:7700', '', {
      placeholderSearch: false,
      primaryKey: 'id',
    });

    const search = instantsearch({
      indexName: 'videos',
      searchClient,
    });

    search.addWidgets([
      searchBox({
        container: '#meili',
        placeholder: 'Search',
        showReset: true,
        showLoadingIndicator: true,
      }),
      customAutocomplete({
        container: document.querySelector('#meili-results'),
      }),
    ]);

    search.start();

    const searchInput = document.querySelector('.ais-SearchBox-input');
    searchInput.addEventListener('keydown', (event) => {
      if (event.keyCode == 13) {
        window.location.href =
          '/search/?results=' + encodeURIComponent(searchInput.value);
      }
    });
  }
});

const indexExists = async () => {
  let client = new MeiliSearch({ host: 'http://localhost:7700' });
  let indexes = await client.getIndexes();
  if (indexes.results.some((e) => e.uid === 'videos')) {
    return true;
  }
  return false;
};

const renderIndexListItem = ({ hits }) => `
  <ul class="list-group list-group-flush">
    ${hits
      .map(
        (hit) =>
          `<li class="list-group-item">
            <a class="link-dark text-decoration-none" href="/search/?results=${
              hit.title
            }"><p>${instantsearch.highlight({
              attribute: 'title',
              hit,
            })}</p></a>
          </li>`,
      )
      .join('')}
  </ul>
`;

const renderAutocomplete = (renderOptions) => {
  const { indices } = renderOptions;
  const container = document.querySelector('#meili-results');

  container.innerHTML = `
    <ul>
      ${indices.map(renderIndexListItem).join('')}
    </ul>
  `;
};

const customAutocomplete = connectAutocomplete(renderAutocomplete);
