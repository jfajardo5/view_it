import '../sass/project.scss';
import { MeiliSearch } from 'meilisearch';
import { instantMeiliSearch } from '@meilisearch/instant-meilisearch';
import instantsearch from 'instantsearch.js';
import { searchBox } from 'instantsearch.js/es/widgets';
import { infiniteHits } from 'instantsearch.js/es/widgets';

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
      initialUiState: {
        videos: {
          query: getParameter(),
        },
      },
    });

    search.addWidgets([
      searchBox({
        container: '#meilisearch',
        placeholder: 'Search',
        showReset: true,
        showLoadingIndicator: true,
      }),
      infiniteHits({
        container: '#hits',
        escapeHTML: true,
        templates: {
          item(hit, { html, components }) {
            return html`
              <article
                class="bg-dark d-flex flex-row justify-content-start align-items-center w-100 h-100"
              >
                <a class="text-light text-decoration-none" href="${hit.url}">
                  <div
                    class="embed-responsive embed-responsive-16by9 bg-black d-flex flex-column justify-content-center align-items-center"
                  >
                    <video
                      poster="${hit.thumbnail}"
                      style="width: 200px; height: 112.50px;"
                    ></video>
                  </div>
                </a>
                <div class="p-2">
                  <a class="text-light text-decoration-none" href="${hit.url}">
                    <h2>
                      ${components.Highlight({ attribute: 'title', hit })}
                    </h2>
                  </a>
                  <small class="fw-bold"
                    >Uploaded by:
                    <a
                      class="text-light text-decoration-none"
                      href="/@${hit.user}"
                      >@${hit.user}</a
                    ></small
                  >
                  <p class="object-fit-contain">${hit.description}</p>
                </div>
              </article>
            `;
          },
        },
      }),
    ]);
    search.start();
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

const getParameter = () => {
  let params = new URLSearchParams(document.location.search);
  return params.get('results');
};
