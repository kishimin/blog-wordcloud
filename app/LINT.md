# frontend・backendのESLint

両パッケージで `bun run lint` を実行できます。修正可能な違反だけを自動修正する場合は `bun run lint:fix` を使います。

`app` から実行する場合は、次のコマンドを使います。

| 対象 | コマンド |
| --- | --- |
| backend | `bun run lint:backend` |
| frontend | `bun run lint:frontend` |
| backend → frontend | `bun run lint` |

最後のコマンドはbackendが成功した場合にfrontendを実行します。既存の `bun run code` はBiomeによる整形・Lint等の検査として残しています。ESLintの追加に伴い、frontendの従来のOxlint設定と依存関係は削除しています。

## 設定の元と適用範囲

[wait-time-calculationのeslint.config.js](https://github.com/kishimin/wait-time-calculation/blob/ab0f440e5abf9f60e5152fba12fb7e5d8e5893a5/frontend/eslint.config.js) を参照しています。

| 設定ファイル | 対象 |
| --- | --- |
| `eslint.config.base.mjs` | JavaScript・TypeScript推奨設定、import順・解決、未使用import、JSDoc |
| `frontend/eslint.config.mjs` | 共通設定とReact・Hooks・Fast Refresh・JSXアクセシビリティ・Testing Library・Vitest |
| `backend/eslint.config.mjs` | 共通設定とBunのテスト。React用のルールは適用しない |

型情報を使うルールは各パッケージの `src/**/*.{ts,tsx}` に適用します。`projectService` と各パッケージの `tsconfigRootDir` を指定し、対応するTypeScriptプロジェクトを利用します。Vite・Storybookの設定ファイルには型情報不要のルールを適用し、Node.jsのグローバル変数を認識させます。

backendのテストは `bun:test` を利用しているため、Vitestプラグインの `vitestImports` に `bun:test` を指定します。これにより、`test.only` などの集中実行指定も検査します。Testing Libraryのルールはfrontendのテストファイルだけに適用します。

`src` 外のテストにも構文ベースのテストルールを適用しますが、TypeScriptプロジェクトの対象外なので、Vitestプラグインの型情報を使う検査はそこで無効にしています。

参照元の `dist` は生成物として除外します。また、カバレッジ・Storybook出力も除外します。参照元固有の `endpoints`・`src/models` の除外は引き継ぎません。frontend内の `playwright@latest` は別のpackageを持つscaffoldなので、今回のViteアプリの検査対象から外しています。

未使用変数は `unused-imports/no-unused-vars`、未使用importは `unused-imports/no-unused-imports` へ集約し、同じ対象への未使用変数ルールの重複適用を避けています。先頭が `_` の変数・引数は参照元と同様に許可します。

## TypeScriptのバージョン

`typescript-eslint` が利用するTypeScript APIと、型チェックに使うコンパイラーをパッケージごとに宣言しています。

| 利用箇所 | 宣言 |
| --- | --- |
| `app` の共通Lintツール | TypeScript `~6.0.3` |
| backendの型チェック | TypeScript `^7.0.2` |
| schemasの型チェック | TypeScript `^7.0.2` |
| frontendの型チェック | 既存のTypeScript `~6.0.3` |

`typescript-eslint` はTypeScript 7のAPIを利用できないため、共通LintツールからはTypeScript 6を解決します。backend・schemasの既存のコンパイラーバージョンは、それぞれの `devDependencies` で維持します。

## 違反が見つかった場合

Lintが起動できることと、既存コードがすべてのルールに適合していることは別です。違反がある場合、`bun run lint` は終了コード1で失敗します。既存コードの違反を隠すためにルールを無効化したり、一括で `--fix` を実行したりはしていません。

ESLintのコマンドはまだCIへ組み込んでいません。
